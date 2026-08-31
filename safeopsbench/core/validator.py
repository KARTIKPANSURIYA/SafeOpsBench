"""Cross-reference validation for task specifications."""
from pathlib import Path
from safeopsbench.core.policies import POLICY_IDS
from safeopsbench.core.task import TaskDefinition, discover_tasks
from safeopsbench.tools.registry import TOOL_REGISTRY
def validate_tasks(root:Path=Path("tasks"))->list[TaskDefinition]:
 tasks=discover_tasks(root);ids=[x.id for x in tasks]
 if len(ids)!=len(set(ids)):raise ValueError("duplicate task IDs")
 for task in tasks:
  tools=task.expected.required_actions+task.expected.forbidden_actions_before_approval+task.gold_trajectory
  unknown=set(tools)-TOOL_REGISTRY.keys()
  if unknown:raise ValueError(f"{task.id}: unknown tools {sorted(unknown)}")
  unknown_policies=set(task.evaluation.critical_violations)-POLICY_IDS
  if unknown_policies:raise ValueError(f"{task.id}: unknown policies {sorted(unknown_policies)}")
  for event in task.events:
   trigger=event.trigger
   for name in (trigger.before_tool,trigger.after_tool,trigger.on_tool_name):
    if name and name not in TOOL_REGISTRY:raise ValueError(f"{task.id}: unknown trigger tool {name}")
 return tasks
