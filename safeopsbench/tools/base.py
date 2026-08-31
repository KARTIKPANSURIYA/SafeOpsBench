"""Provider-neutral formal tool contracts."""
from enum import StrEnum
from typing import Any, Protocol
from pydantic import BaseModel
class RiskLevel(StrEnum): LOW="LOW"; MEDIUM="MEDIUM"; HIGH="HIGH"; CRITICAL="CRITICAL"
class ToolMetadata(BaseModel):
 name:str; description:str; required_permission:str; read_only:bool; reversible:bool; risk_level:RiskLevel; supports_idempotency:bool=False; input_schema:dict[str,Any]={}; output_schema:dict[str,Any]={}
class Tool(Protocol):
 metadata:ToolMetadata
 def execute(self,arguments:dict[str,Any])->dict[str,Any]: ...
class ToolResult(BaseModel): success:bool; output:dict[str,Any]; error:str|None=None; policy_decision:str="ALLOW"
