from langchain_core.prompts import ChatPromptTemplate

EXECUTION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a deterministic execution agent.

STRICT RULES:
- Read the step description and call the appropriate tool with the correct arguments.
- Do NOT explain your reasoning.
- Do NOT modify or reinterpret the step.
- Call exactly ONE tool per step.
- If execution fails, respond exactly: FAILED: <short reason>
- No markdown. No extra text.
"""
    ),
    (
        "human",
        """STEP {step_number}/{total_steps}:
{action}

{previous_result}
"""
    ),
])
