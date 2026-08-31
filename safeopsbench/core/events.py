"""Deterministic environment event controller."""
from collections import Counter
from typing import Any
from safeopsbench.core.task import EventSpec
class EventController:
 def __init__(self,events:list[EventSpec]): self.events=events; self.fired:set[int]=set(); self.failures:Counter[str]=Counter()
 def matching(self,when:str,tool:str,step:int)->list[tuple[int,EventSpec]]:
  out=[]
  for i,event in enumerate(self.events):
   if i in self.fired: continue
   t=event.trigger
   if (when=="before" and t.before_tool==tool) or (when=="after" and t.after_tool==tool) or t.on_tool_name==tool or (t.after_n_steps is not None and step>=t.after_n_steps): self.fired.add(i); out.append((i,event))
  return out
