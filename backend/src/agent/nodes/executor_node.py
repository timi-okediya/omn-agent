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
        reflection_passed = state.get("reflection_passed", True)

        last_tool_result = state.get("last_tool_result")
        if messages and isinstance(messages[-1], ToolMessage):
            last_tool_result = messages[-1].content

        if not reflection_passed and current_step > 0:
            current_step = current_step - 1

        if current_step >= len(plan):
            return {
                "last_tool_result": last_tool_result,
                "user_message": "All steps completed"
            }

        if current_step >= max_steps:
            return {
                "messages": [SystemMessage(content="FAILED: Max steps reached.")],
                "user_message": "Max steps reached"
            }

        step: PlanStep = plan[current_step]

        messages_prompt = EXECUTION_PROMPT.format_messages(
            action=step.action,
            step_number=current_step + 1,
            total_steps=len(plan),
            previous_result=f"PREVIOUS RESULT: {last_tool_result}" if last_tool_result else "",
        )

        result = llm.invoke(messages_prompt)

        # print("\n===== EXECUTOR OUTPUT =====")
        # print(result)

        if hasattr(result, "tool_calls") and result.tool_calls:
            tool_name = result.tool_calls[0].get("name", "unknown")
            return {
                "messages": [result],
                "current_step": current_step + 1,
                "last_tool_result": last_tool_result,
                "reflection_passed": True,
                "user_message": f"Executing step {current_step + 1}/{len(plan)}: {step.action} -> Calling {tool_name}..."
            }

        return {
            "messages": [result],
            "current_step": current_step + 1,
            "last_tool_result": result.content if hasattr(result, "content") else str(result),
            "reflection_passed": True,
            "user_message": f"Step {current_step + 1}/{len(plan)} result: {result.content[:100]}..." if hasattr(result, "content") else "Step completed"
        }

    return _node
