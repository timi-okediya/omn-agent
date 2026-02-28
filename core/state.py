from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage, SystemMessage
from pydantic import BaseModel

from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage, SystemMessage
from pydantic import BaseModel


class PlanStep(BaseModel):
    action: str
    args: Dict[str, Any]


class AgentState(TypedDict):
    messages: List[BaseMessage]
    plan: Optional[List[PlanStep]]
    current_step: int
    max_steps: int
    safety_passed: bool
    last_tool_result: Optional[str]


initial_state: AgentState = {
    "messages": [],
    "plan": None,
    "current_step": 0,
    "max_steps": 10,
    "safety_passed": False,
    "last_tool_result": None,
}
