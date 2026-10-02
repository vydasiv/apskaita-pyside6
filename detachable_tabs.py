from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QTabWidget, QWidget, QMainWindow, QVBoxLayout, QMenuBar, QMenu
)

class DetachedWindow(QMainWindow):
    def __init__(self, owner_tabs, widget, title, original_index):
        super().__init__()
        self._owner_tabs = owner_tabs
        self._widget = widget
        self._title = title
        self._original_index = original_index
        self.setWindowTitle(title)
        self.resize(1100, 750)
        self.setCentralWidget(widget)
        self._init_menu()

    def _init_menu(self):
        mb = self.menuBar()
        m = mb.addMenu('Kortelė')
        act = m.addAction('Grąžinti į pagrindinį langą')
        act.triggered.connect(self.close)

    def closeEvent(self, event):
        if not getattr(self._owner_tabs, '_is_shutting_down', False):
            self.takeCentralWidget()
            self._owner_tabs._reattach(self._widget, self._title, self._original_index, self)
        event.accept()

class DetachableTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._detached = {}
        self._order = []
        self._is_shutting_down = False
        tb = self.tabBar()
        tb.setContextMenuPolicy(Qt.CustomContextMenu)
        tb.customContextMenuRequested.connect(self._open_context_menu)

    def addTab(self, widget, title):
        idx = super().addTab(widget, title)
        if title not in self._order:
            self._order.append(title)
        return idx

    def _open_context_menu(self, pos: QPoint):
        tb = self.tabBar()
        idx = tb.tabAt(pos)
        if idx < 0:
            return
        m = QMenu(self)
        act = m.addAction('Atkabinti į atskirą langą')
        act.triggered.connect(lambda: self.detach_tab(idx))
        m.exec(tb.mapToGlobal(pos))

    def detach_tab(self, index: int):
        if index < 0 or index >= self.count():
            return
        title = self.tabText(index)
        widget = self.widget(index)
        self.removeTab(index)
        win = DetachedWindow(self, widget, title, index)
        self._detached[title] = win
        win.show()

    def _reattach(self, widget, title, original_index, win):
        if title in self._detached:
            del self._detached[title]
        target_idx = self._target_index(title)
        self.insertTab(target_idx, widget, title)
        self.setCurrentIndex(target_idx)

    def _target_index(self, title: str) -> int:
        if title not in self._order:
            return self.count()
        rank = self._order.index(title)
        present = [self.tabText(i) for i in range(self.count())]
        return sum(1 for t in present if t in self._order and self._order.index(t) < rank)

    def close_detached(self):
        self._is_shutting_down = True
        for win in list(self._detached.values()):
            win.close()
