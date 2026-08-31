"""Repeated-run reliability statistics."""


def consistency(values: list[bool]) -> float:
    if not values:
        return 0.0
    rate = sum(values) / len(values)
    return max(rate, 1 - rate)


def pass_k(values: list[bool]) -> float:
    return float(all(values)) if values else 0.0
