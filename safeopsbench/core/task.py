"""Versioned YAML benchmark task schema and validation."""
from pathlib import Path
from typing import Any
import yaml
from pydantic import BaseModel, Field
class AgentSpec(BaseModel): role:str="sales_rep"
class Trigger(BaseModel): before_tool:str|None=None; after_tool:str|None=None; after_n_steps:int|None=None; on_tool_name:str|None=None; at_timestamp:str|None=None
class EventSpec(BaseModel): type:str; trigger:Trigger; payload:dict[str,Any]=Field(default_factory=dict)
class Goal(BaseModel): status:str
class Expected(BaseModel): goal:Goal; required_actions:list[str]=Field(default_factory=list); forbidden_actions_before_approval:list[str]=Field(default_factory=list); final_state_constraints:dict[str,Any]=Field(default_factory=dict)
class EvaluationSpec(BaseModel): critical_violations:list[str]=Field(default_factory=list); minimum_tool_calls:int=1
class TaskDefinition(BaseModel):
    schema_version:str="0.1"; id:str=Field(pattern=r"^C\d{3}$"); name:str; category:str; domain:str="commerce"; difficulty:int=Field(ge=1,le=5); user_request:str; agent:AgentSpec=Field(default_factory=AgentSpec); initial_state:dict[str,Any]=Field(default_factory=dict); task_parameters:dict[str,Any]=Field(default_factory=dict); events:list[EventSpec]=Field(default_factory=list); expected:Expected; evaluation:EvaluationSpec=Field(default_factory=EvaluationSpec); gold_trajectory:list[str]=Field(default_factory=list)
def load_task(path:Path)->TaskDefinition:
    data=yaml.safe_load(path.read_text()); return TaskDefinition.model_validate(data)
def discover_tasks(root:Path=Path("tasks"))->list[TaskDefinition]: return [load_task(p) for p in sorted(root.rglob("*.yaml"))]
