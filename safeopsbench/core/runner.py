"""Agent/environment execution loop."""
from safeopsbench.agents.base import FinalResponseAction, Observation
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.evaluator import EvaluationResult, evaluate
from safeopsbench.core.trajectory import StepType
def run_agent(env:SafeOpsEnvironment,agent:object,max_steps:int=30)->EvaluationResult:
 agent.reset() # type: ignore[attr-defined]
 latest=None
 for i in range(max_steps):
  obs=Observation(user_request=env.task.user_request,available_tools=env.available_tools,latest_tool_result=latest,relevant_policy_context=["Authorization and enterprise policies are enforced authoritatively."],step_number=i)
  action=agent.act(obs) # type: ignore[attr-defined]
  if isinstance(action,FinalResponseAction):env.trajectory.add(StepType.AGENT_MESSAGE,output={"message":action.message});break
  result=env.execute_tool(action.tool_name,action.arguments);latest=result.model_dump(mode="json")
 return evaluate(env)
