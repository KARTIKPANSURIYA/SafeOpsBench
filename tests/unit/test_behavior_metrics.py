"""Metric denominator and null-semantics tests."""

from types import SimpleNamespace

from safeopsbench.metrics.scoring import aggregate


def result(**overrides: object) -> SimpleNamespace:
    values = {
        "task_success": True,
        "safe_success": True,
        "policy_violations": [],
        "state_valid": True,
        "unauthorized_actions": 0,
        "recovered_failures": 0,
        "recoverable_failures": 0,
        "tool_calls": 4,
        "attempted_consequential_actions": 2,
        "unsafe_action_attempts": 1,
        "policy_relevant_action_attempts": 2,
        "blocked_unsafe_actions": 1,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


def test_uaar_and_policy_adherence_use_action_denominators() -> None:
    metrics = aggregate([result()])
    assert metrics.unsafe_action_attempt_rate == 0.5
    assert metrics.policy_adherence_rate == 0.5
    assert metrics.average_blocked_unsafe_actions == 1.0


def test_behavior_rates_are_null_without_relevant_attempts() -> None:
    metrics = aggregate(
        [
            result(
                attempted_consequential_actions=0,
                unsafe_action_attempts=0,
                policy_relevant_action_attempts=0,
            )
        ]
    )
    assert metrics.unsafe_action_attempt_rate is None
    assert metrics.policy_adherence_rate is None
