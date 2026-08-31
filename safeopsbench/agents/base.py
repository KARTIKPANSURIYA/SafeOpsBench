"""Provider-neutral agent protocol and leakage-safe observations."""
from typing import Annotated, Any, Literal, Protocol
from pydantic import BaseModel, Field
class Observation(BaseModel): user_request:str; available_tools:list[dict[str,Any]]; latest_tool_result:dict[str,Any]|None=None; relevant_policy_context:list[str]=Field(default_factory=list); step_number:int
class ToolCallAction(BaseModel): type:Literal["tool_call"]="tool_call"; tool_name:str; arguments:dict[str,Any]
class FinalResponseAction(BaseModel): type:Literal["final_response"]="final_response"; message:str
AgentAction=Annotated[ToolCallAction|FinalResponseAction,Field(discriminator="type")]
class Agent(Protocol):
 @property
 def agent_id(self)->str:...
 def reset(self)->None:...
 def act(self,observation:Observation)->ToolCallAction|FinalResponseAction:...
