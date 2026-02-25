from core.state import AgentState
from prompts import SAFETY_PROMPT
from llm import LLM
from pydantic import BaseModel
import json
import re

from prompts.safety_prompt import SAFETY_PROMPT_FORMAT_INSTRUCTIONS
from schemas.safety import SafetyCheck

BLOCKED_KEYWORDS = [
    "rm -rf",
    "format disk",
    "delete /",
    "shutdown",
    "reboot",
]



def safety_check(llm: LLM):
    def _node(state: AgentState):
        try:
            blocked_keywords_str = "\n".join(f"- {kw}" for kw in BLOCKED_KEYWORDS)
            task = state["messages"][-1].content

            messages = SAFETY_PROMPT.format_messages(
                task=task,
                blocked_keywords=blocked_keywords_str,
                format_instructions=SAFETY_PROMPT_FORMAT_INSTRUCTIONS,
            )

            result = llm.invoke(messages=messages)

            raw = result.content
            cleaned = re.sub(r"```json|```", "", raw).strip()

            content = json.loads(cleaned)
            print(content)

            return {
                **state,
                "user_input": state["messages"][-1].content,
                "safe": content.get("is_safe", False),
            }

        except Exception as e:
            print("Safety parsing failed:", e)
            print("Raw output:", result.content if "result" in locals() else "No result")

            # Fail closed
            return {
                **state,
                "safe": False,
                "safety_reason": "Safety parsing failed"
            }

    return _node
