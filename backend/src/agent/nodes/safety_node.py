from core import AgentState
from prompts.safety_prompt import SAFETY_PROMPT, SAFETY_PROMPT_FORMAT_INSTRUCTIONS
from llm import LLM
import json


BLOCKED_KEYWORDS = [
    # File system destruction
    "rm -rf", "rmdir", "del /f", "del /s", "format", "mkfs",
    "shred", "wipe", "overwrite", "truncate",
    # Database destruction
    "DROP TABLE", "DROP DATABASE", "TRUNCATE TABLE",
    "DELETE FROM", "DESTROY DATABASE",
    # System/shell abuse
    "sudo", "chmod 777", "chown", ":(){:|:&};:",
    "dd if=", "fork bomb", "kill -9", "killall",
    # Code execution / injection
    "exec(", "eval(", "os.system(", "subprocess",
    "shell=True", "__import__", "base64.decode",
    # Network abuse
    "reverse shell", "nc -e", "ncat", "curl | bash", "wget | sh",
    # Secrets / env abuse
    "cat /etc/passwd", "cat /etc/shadow", ".env",
    "print(os.environ)", "dump credentials", "export secrets",
]


def safety_check(llm: LLM):
    def _node(state: AgentState):

        blocked_keywords_str = "\n".join(f"- {kw}" for kw in BLOCKED_KEYWORDS)
        task = state["messages"][-1].content

        messages = SAFETY_PROMPT.format_messages(
            task=task,
            blocked_keywords=blocked_keywords_str,
            format_instructions=SAFETY_PROMPT_FORMAT_INSTRUCTIONS,
        )

        result = llm.invoke(messages)

        raw = result.content
        print(raw)

        try:
            content = json.loads(raw)

            return {
                "safety_passed": content.get("is_safe", False)
            }

        except Exception:
            # Fail CLOSED (safe default)
            return {
                "safety_passed": False
            }

    return _node
