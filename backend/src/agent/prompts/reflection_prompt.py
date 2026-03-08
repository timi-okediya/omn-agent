from langchain_core.prompts import ChatPromptTemplate

REFLECTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an iterative reflection agent. After each step execution, "
        "evaluate if the current progress is correct and decide if more work is needed.\n\n"
        "If the task portion is done well so far, respond:\n"
        "REFLECTION: PASS\n"
        "PROGRESS: <what was accomplished>\n\n"
        "If issues remain and need fixing, respond:\n"
        "REFLECTION: FAIL\n"
        "ISSUES: <what went wrong>\n"
        "FIX: <how to correct it>"
    ),
    (
        "human",
        """CURRENT STEP RESULT:
{tool_results_str}

REFLECTION HISTORY:
{reflection_history}

Should execution continue or retry?"""
    ),
])
