from langchain_core.prompts import ChatPromptTemplate

REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are the final review agent. "
        "Determine if the task has been completed successfully based on all execution history. "
        "Look at the reflection feedback and determine if the overall task is done.\n\n"
        "Respond exactly with:\n"
        "STATUS: COMPLETE - <brief summary>\n\n"
        "Or if fundamentally incomplete:\n"
        "STATUS: INCOMPLETE\n"
        "REASON: <why it failed>"
    ),
    (
        "human",
        """TASK:
{task}

PLAN:
{plan_summary}

REFLECTION HISTORY:
{reflection_history}

TOOL RESULTS:
{tool_results_str}

Final review."""
    ),
])
