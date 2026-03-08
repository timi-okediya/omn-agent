from core import AgentState
from langchain_core.messages import ToolMessage
from prompts import REFLECTION_PROMPT


def reflection(llm):
    def _node(state: AgentState):
        messages = state.get("messages", [])
        reflection_history = state.get("reflection", "")

        tool_results = [
            f"- {m.name}: {m.content}"
            for m in messages
            if isinstance(m, ToolMessage)
        ]
        tool_results_str = "\n".join(tool_results) if tool_results else "No tool results yet."

        formatted_messages = REFLECTION_PROMPT.format_messages(
            tool_results_str=tool_results_str,
            reflection_history=reflection_history or "No previous reflections.",
        )

        response = llm.invoke(formatted_messages)

        passed = "REFLECTION: PASS" in (response.content or "").upper()

        return {
            "messages": [response],
            "reflection": response.content,
            "reflection_passed": passed,
        }

    return _node
