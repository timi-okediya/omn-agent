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

    # Structured planning
    plan: Optional[List[PlanStep]]
    current_step: int
    max_steps: int

    # Safety
    safety_passed: bool

    # Execution tracking
    last_tool_result: Optional[str]


initial_state: AgentState = {
    "messages": [
        SystemMessage(
            content="""
You are a strict automation assistant.

CRITICAL RULES:

1. Call a tool ONLY when required.
2. NEVER call the same tool more than once per request.
3. After a successful tool result, do NOT call it again.
4. If a tool result satisfies the request, respond normally.
5. Do NOT retry tools unless explicitly asked.
6. Be concise.
7. Do not invent tool outputs.

Tool Usage Rules:
- Use ping_server ONLY when checking server status.
- Use create_folder ONLY when explicitly asked.
- Do NOT guess or repeat actions.
"""
        )
    ],
    "plan": None,
    "current_step": 0,
    "max_steps": 10,
    "safety_passed": False,
    "last_tool_result": None,
}
