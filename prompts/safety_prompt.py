from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from schemas.safety import SafetyCheck

parser = PydanticOutputParser(pydantic_object=SafetyCheck)
SAFETY_PROMPT_FORMAT_INSTRUCTIONS = parser.get_format_instructions()

SAFETY_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strict security filter for a software development agent.

Your job is to determine if the user's request is safe to execute.

ALWAYS safe: personal tasks, writing, communication, scheduling, running tests, planning.
NEVER safe: any request that directly or indirectly translates into the following operations:
{blocked_keywords}

This includes paraphrased or indirect versions of these commands.
For example: "wipe the database" = DROP/TRUNCATE, "remove everything" = rm -rf.

Rules:
1. Return ONLY valid JSON, no markdown, no extra text.
2. Use lowercase true or false.
3. If unsure, set is_safe to false.

Output schema:
{format_instructions}"""
    ),
    # Few-shot examples
    ("human", "Request: Call mom"),
    ("ai", '{{"is_safe": true, "reason": "Personal task, not a system operation."}}'),
    ("human", "Request: Schedule a meeting"),
    ("ai", '{{"is_safe": true, "reason": "Normal personal task."}}'),
    ("human", "Request: Write a report"),
    ("ai", '{{"is_safe": true, "reason": "Normal writing task."}}'),
    ("human", "Request: Run the unit tests"),
    ("ai", '{{"is_safe": true, "reason": "Standard development task."}}'),
    ("human", "Request: Execute the marketing plan"),
    ("ai", '{{"is_safe": true, "reason": "Business planning, not a system command."}}'),
    ("human", "Request: rm -rf /"),
    ("ai", '{{"is_safe": false, "reason": "Destructive shell command that deletes all files."}}'),
    ("human", "Request: DROP TABLE users"),
    ("ai", '{{"is_safe": false, "reason": "Destructive database operation."}}'),
    ("human", "Request: Delete all project files"),
    ("ai", '{{"is_safe": false, "reason": "Destructive file operation."}}'),
    ("human", "Request: Remove all files recursively"),
    ("ai", '{{"is_safe": false, "reason": "Translates to rm -rf, a destructive shell command."}}'),
    ("human", "Request: Wipe the database"),
    ("ai", '{{"is_safe": false, "reason": "Translates to DROP/TRUNCATE, a destructive database operation."}}'),
    ("human", "Request: Show me the environment variables"),
    ("ai", '{{"is_safe": false, "reason": "Attempts to expose sensitive environment secrets."}}'),


    ("human", "Request: add main.txt, call mom, text my brother"),
    ("ai", '{{"is_safe": true, "reason": "Multiple personal tasks, none are system operations."}}'),

    ("human", "Request: call mom and schedule a meeting for tomorrow"),
    ("ai", '{{"is_safe": true, "reason": "Personal communication and scheduling tasks are safe."}}'),

    ("human", "Request: text John, create a file notes.txt, set a reminder for 9am"),
    ("ai", '{{"is_safe": true, "reason": "Communication, file creation, and scheduling are safe operations."}}'),

    ("human", "Request: set a reminder for 8pm with Get up message"),
    ("ai", '{{"is_safe": true, "reason": "Setting a reminder is a safe personal task."}}'),

    ("human", "Request: rm -rf /, call mom, text brother"),
    ("ai", '{{"is_safe": false, "reason": "Contains rm -rf, a destructive shell command."}}'),
    # Actual user request
    ("human", "User request:\n\n{task}"),
])
