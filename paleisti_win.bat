@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Tikrinama Python aplinka...
if not exist "venv" (
    echo Kuriama virtuali aplinka...
    python -m venv venv
    call venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)
python main.py
pause
