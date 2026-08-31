from safeopsbench.agents.deterministic import RuleBasedSafeAgent
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import discover_tasks
from safeopsbench.metrics.scoring import aggregate
results=[]
for task in discover_tasks():
 env=SafeOpsEnvironment(task,"example");results.append(run_agent(env,RuleBasedSafeAgent()));env.close()
print(aggregate(results).model_dump_json(indent=2))
