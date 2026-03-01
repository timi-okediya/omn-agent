from core import AgentState
from core.state import PlanStep
from llm import LLM
from langchain_core.messages import SystemMessage
from prompts.executor_prompt import EXECUTION_PROMPT
from langchain_core.messages import ToolMessage


def executor(llm: LLM):
    def _node(state: AgentState):

        current_step = state.get("current_step", 0)
        max_steps = state.get("max_steps", 10)
        plan = state.get("plan") or []
        messages = state.get("messages", [])

        # ← Capture tool result if last message is a ToolMessage
        last_tool_result = state.get("last_tool_result")
        if messages and isinstance(messages[-1], ToolMessage):
            last_tool_result = messages[-1].content

        if current_step >= len(plan):
            return {"last_tool_result": last_tool_result}

        if current_step >= max_steps:
            return {
                "messages": [SystemMessage(content="FAILED: Max steps reached.")]
            }

        step: PlanStep = plan[current_step]

        messages_prompt = EXECUTION_PROMPT.format_messages(
            action=step.action,
            step_number=current_step + 1,
            total_steps=len(plan),
            previous_result=f"PREVIOUS RESULT: {last_tool_result}" if last_tool_result else "",
        )

        result = llm.invoke(messages_prompt)

        print("\n===== EXECUTOR OUTPUT =====")
        print(result)

        if hasattr(result, "tool_calls") and result.tool_calls:
            return {
                "messages": [result],
                "current_step": current_step + 1,
                "last_tool_result": last_tool_result,  # preserve until tool runs
            }

        return {
            "messages": [result],
            "current_step": current_step + 1,
            "last_tool_result": result.content if hasattr(result, "content") else str(result),
        }

    return _node
