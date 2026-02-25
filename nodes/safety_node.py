from core.state import AgentState
from prompts import SAFETY_PROMPT
from llm import LLM
from pydantic import BaseModel

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
        blocked_keywords_str = "\n".join(f"- {kw}" for kw in BLOCKED_KEYWORDS)
        task = state["messages"][-1].content
        messages = SAFETY_PROMPT.format_messages(
            task=task,
            blocked_keywords=blocked_keywords_str,
            format_instructions=SAFETY_PROMPT_FORMAT_INSTRUCTIONS,
        )
        result = llm.invoke(
            messages=messages,
        )

        print(result)

    #     blocked_keywords = ["rm -rf", "format", "delete /", "shutdown"]

    #     for word in blocked_keywords:
    #         if word in user_message:
    #             return {
    #                 "safety_passed": False,
    #                 "messages": [
    #                     llm.invoke("Refuse politely. Dangerous request.")
    #                 ],
    #             }

    #     return {"safety_passed": True}

    return _node
