"""Provider-neutral agent/environment execution loop."""

from safeopsbench.agents.base import Agent, FinalResponseAction, Observation
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.evaluator import EvaluationResult, evaluate
from safeopsbench.core.trajectory import StepType


def run_agent(
    environment: SafeOpsEnvironment, agent: Agent, max_steps: int = 30
) -> EvaluationResult:
    """Run an agent without exposing task-specific evaluation expectations."""
    agent.reset()
    latest: dict[str, object] | None = None
    for step_number in range(max_steps):
        observation = Observation(
            user_request=environment.task.user_request,
            available_tools=environment.available_tools,
            latest_tool_result=latest,
            relevant_policy_context=[
                "Authorization and enterprise policies are enforced authoritatively."
            ],
            step_number=step_number,
        )
        action = agent.act(observation)
        if isinstance(action, FinalResponseAction):
            environment.trajectory.add(StepType.AGENT_MESSAGE, output={"message": action.message})
            break
        result = environment.execute_tool(action.tool_name, action.arguments)
        latest = result.model_dump(mode="json")
    return evaluate(environment)
