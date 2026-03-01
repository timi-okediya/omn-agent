from langchain_core.prompts import ChatPromptTemplate

REVIEW_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a reflection agent. "
        "Evaluate whether the plan was executed successfully. "
        "If successful, respond with:\n"
        "STATUS: COMPLETE\n"
        "If not successful, respond with:\n"
        "STATUS: INCOMPLETE\n"
        "REASON: <what failed>\n"
        "SUGGESTION: <how to fix it>\n"
        "Always include the tool results."
    ),
    (
        "human",
        """PLAN:
{plan_summary}

TOOL RESULTS:
{tool_results_str}

Evaluate execution."""
    ),
])
