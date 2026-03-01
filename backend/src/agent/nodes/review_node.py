from core import AgentState
from langchain_core.messages import ToolMessage
from prompts import REVIEW_PROMPT


def review(llm):
    def _node(state: AgentState):
        plan = state.get("plan") or []
        messages = state.get("messages") or []
        last_tool_result = state.get("last_tool_result", "No result recorded.")
        retry_count = state.get("retry_count", 0)

        # Collect all tool results from message history
        tool_results = [
            f"- {m.name}: {m.content}"
            for m in messages
            if isinstance(m, ToolMessage)
        ]
        tool_results_str = "\n".join(tool_results) if tool_results else last_tool_result

        # Summarize plan
        plan_summary = "\n".join(
            f"- Step {i+1}: {step.action}"
            for i, step in enumerate(plan)
        )

        # 🔥 Use ChatPromptTemplate properly
        formatted_messages = REVIEW_PROMPT.format_messages(
            plan_summary=plan_summary,
            tool_results_str=tool_results_str,
        )

        response = llm.invoke(formatted_messages)

        passed = "COMPLETE" in (response.content or "").upper()

        return {
            "messages": [response],
            "review_passed": passed,
            "retry_count": retry_count + 1,
        }

    return _node
