from typing import TypedDict, List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from pydantic import BaseModel


class PlanStep(BaseModel):
    action: str


class AgentState(TypedDict):
    messages: List[BaseMessage]
    plan: Optional[List[PlanStep]]
    current_step: int
    max_steps: int
    safety_passed: bool
    review_passed: bool
    last_tool_result: Optional[str]
    retry_count: int
    reflection: Optional[str]
    reflection_passed: bool


initial_state: AgentState = {
    "messages": [],
    "plan": None,
    "current_step": 0,
    "max_steps": 10,
    "safety_passed": False,
    "review_passed": False,
    "last_tool_result": None,
    "retry_count": 0,
    "reflection": None,
    "reflection_passed": False,
}
