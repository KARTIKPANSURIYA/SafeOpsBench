"""Seeded random sanity baseline."""
import random
from safeopsbench.agents.base import FinalResponseAction, Observation, ToolCallAction
class RandomToolAgent:
 agent_id="random"
 def __init__(self,seed:int=42):self.random=random.Random(seed);self.steps=0
 def reset(self)->None:self.steps=0
 def act(self,o:Observation)->ToolCallAction|FinalResponseAction:
  self.steps+=1
  if self.steps>4:return FinalResponseAction(message="Random baseline stopped.")
  name=self.random.choice([x["name"] for x in o.available_tools])
  return ToolCallAction(tool_name=name,arguments={})
