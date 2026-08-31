from safeopsbench.agents.deterministic import RuleBasedSafeAgent,ScriptedCorrectAgent
from safeopsbench.core.environment import SafeOpsEnvironment
from safeopsbench.core.runner import run_agent
from safeopsbench.core.task import discover_tasks
def outcomes(cls):
 out=[]
 for t in discover_tasks():
  e=SafeOpsEnvironment(t,"baseline");out.append(run_agent(e,cls()).safe_success);e.close()
 return out
def test_scripted_safe_success():assert sum(outcomes(ScriptedCorrectAgent))/10>=.9
def test_rule_based_has_no_critical_violations():assert all(outcomes(RuleBasedSafeAgent))
