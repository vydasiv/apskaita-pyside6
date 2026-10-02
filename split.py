from decimal import Decimal, ROUND_HALF_UP

def allocate_percent_parts(total: Decimal, percentages: list) -> list:
    s = sum(percentages)
    if s == 0:
        return [Decimal('0.00')] * len(percentages)
    cents = total * Decimal('100')
    allocated = []
    remainders = []
    for i, p in enumerate(percentages):
        raw = cents * (p / s)
        base = int(raw)
        rem = raw - Decimal(base)
        allocated.append(base)
        remainders.append((rem, i))
    diff = int(cents) - sum(allocated)
    remainders.sort(key=lambda x: x[0], reverse=True)
    for k in range(diff):
        allocated[remainders[k][1]] += 1
    return [Decimal(x) / Decimal('100') for x in allocated]
