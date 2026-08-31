from safeopsbench.agents.deterministic import RuleBasedSafeAgent
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import discover_tasks
task=next(t for t in discover_tasks() if t.id=="C002")
env=SafeOpsEnvironment(task,"example")
print(run_agent(env,RuleBasedSafeAgent()).model_dump_json(indent=2))
env.close()
