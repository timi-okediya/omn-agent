from core import AgentState
from langchain_core.messages import ToolMessage
from prompts import REVIEW_PROMPT


def review(llm):
    def _node(state: AgentState):
        messages = state.get("messages", [])
        plan = state.get("plan") or []
        last_tool_result = state.get("last_tool_result", "No result recorded.")
        reflection_history = state.get("reflection", "No reflections yet.")
        retry_count = state.get("retry_count", 0)

        task = messages[0].content if messages else "Unknown task"

        tool_results = [
            f"- {m.name}: {m.content}"
            for m in messages
            if isinstance(m, ToolMessage)
        ]
        tool_results_str = "\n".join(tool_results) if tool_results else last_tool_result

        plan_summary = "\n".join(
            f"- Step {i+1}: {step.action}"
            for i, step in enumerate(plan)
        )

        formatted_messages = REVIEW_PROMPT.format_messages(
            task=task,
            plan_summary=plan_summary,
            tool_results_str=tool_results_str,
            reflection_history=reflection_history,
        )

        response = llm.invoke(formatted_messages)

        passed = "STATUS: COMPLETE" in (response.content or "").upper()

        return {
            "messages": [response],
            "review_passed": passed,
            "retry_count": retry_count + 1,
            "user_message": f"Final review: {'Complete' if passed else 'Incomplete'} - {response.content[:100]}..." if response.content else "Final review..."
        }

    return _node
