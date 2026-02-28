from langchain_core.prompts import ChatPromptTemplate

PLANNER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """
You are a planning agent.

Return ONLY valid JSON.
Do not explain.
Do not add markdown.
Do not add comments.

Format:
{{
  "steps": [
    {{
      "action": "action name",
      "args": {{"key": "value"}}
    }}
  ]
}}
"""),
    ("human", "{task}")
])
