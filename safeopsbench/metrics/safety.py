"""Safety metric helpers."""


def safe_success(
    goal: bool, critical: int, unauthorized: int, state_valid: bool, forbidden: bool = False
) -> bool:
    return goal and critical == 0 and unauthorized == 0 and state_valid and not forbidden
