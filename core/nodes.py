from core import AgentState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage, ToolMessage


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

        plan_summary = "\n".join(
            f"- Step {i+1}: {step.action}"
            for i, step in enumerate(plan)
        )

        prompt = [
            SystemMessage(content=(
                "You are a review agent. "
                "Check if all planned steps were completed successfully based on the tool results. "
                "Reply with COMPLETE if everything is done. "
                "Otherwise reply with INCOMPLETE: <reason>. "
                "Always include the actual tool results in your response."
            )),
            HumanMessage(content=f"""
PLAN:
{plan_summary}

TOOL RESULTS:
{tool_results_str}

Were all steps completed successfully? Include the tool results in your response.
""")
        ]

        response = llm.invoke(prompt)
        passed = "COMPLETE" in (response.content or "").upper()

        # Build a human-readable summary to print
        summary = f"\n{'='*40}\n"
        summary += "TASK RESULTS:\n"
        summary += f"{tool_results_str}\n"
        summary += f"\nREVIEW: {response.content}\n"
        summary += f"{'='*40}\n"
        print(summary)

        return {
            "messages": [response],
            "review_passed": passed,
            "retry_count": retry_count + 1,
        }

    return _node

def responder():
    def _node(state: AgentState):
        messages = state.get("messages") or []
        plan = state.get("plan") or []

        tool_results = [
            m for m in messages if isinstance(m, ToolMessage)
        ]

        lines = ["Here's what was done:\n"]
        for i, (step, result) in enumerate(zip(plan, tool_results)):
            lines.append(f"Step {i+1}: {step.action}")
            lines.append(f"Result: {result.content}\n")

        summary = "\n".join(lines)

        return {
            "messages": [AIMessage(content=summary)]
        }

    return _node
