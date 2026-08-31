"""Stable trajectory representation."""
from datetime import datetime, timezone
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, Field
class StepType(StrEnum): AGENT_MESSAGE="AGENT_MESSAGE"; TOOL_CALL="TOOL_CALL"; TOOL_RESULT="TOOL_RESULT"; ENVIRONMENT_EVENT="ENVIRONMENT_EVENT"; POLICY_DECISION="POLICY_DECISION"; VIOLATION="VIOLATION"; SYSTEM_EVENT="SYSTEM_EVENT"
class TrajectoryStep(BaseModel):
    step_number:int; timestamp:datetime=Field(default_factory=lambda:datetime.now(timezone.utc)); type:StepType
    tool_name:str|None=None; input:dict[str,Any]|None=None; output:dict[str,Any]|None=None; state_hash:str|None=None; latency_ms:float|None=None; cost:float|None=None; input_tokens:int|None=None; output_tokens:int|None=None
class Trajectory(BaseModel):
    schema_version:str="0.1"; task_run_id:str; steps:list[TrajectoryStep]=Field(default_factory=list)
    def add(self,kind:StepType,**values:Any)->TrajectoryStep:
        step=TrajectoryStep(step_number=len(self.steps)+1,type=kind,**values); self.steps.append(step); return step
