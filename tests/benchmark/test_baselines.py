"""Whole-suite deterministic baseline sanity checks."""

from safeopsbench.agents.deterministic import (
    NaiveOrderAgent,
    RuleBasedSafeAgent,
    ScriptedCorrectAgent,
)
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import discover_tasks


def outcomes(agent_type):
    results = []
    for task in discover_tasks():
        agent = agent_type()
        environment = SafeOpsEnvironment(task, agent.agent_id)
        results.append(run_agent(environment, agent))
        environment.close()
    return results


def test_scripted_agent_validates_task_solvability() -> None:
    assert all(result.safe_success for result in outcomes(ScriptedCorrectAgent))


def test_rule_based_agent_has_no_unsafe_attempts() -> None:
    results = outcomes(RuleBasedSafeAgent)
    assert all(result.safe_success for result in results)
    assert sum(result.unsafe_action_attempts for result in results) == 0


def test_naive_agent_is_behaviorally_distinct() -> None:
    results = outcomes(NaiveOrderAgent)
    assert sum(result.unsafe_action_attempts for result in results) >= 4
    assert sum(result.blocked_unsafe_actions for result in results) >= 4
