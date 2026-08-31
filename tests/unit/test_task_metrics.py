from safeopsbench.core.task import discover_tasks
from safeopsbench.metrics.scoring import tool_efficiency
def test_all_tasks_parse():assert [x.id for x in discover_tasks()]==[f"C{i:03}" for i in range(1,11)]
def test_efficiency_is_bounded():assert tool_efficiency(10,5)==1 and tool_efficiency(5,10)==.5
