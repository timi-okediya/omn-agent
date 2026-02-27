from core.state import AgentState
from prompts.planner_prompt import PLANNER_PROMPT
import json

def planner(llm):
    def _node(state: AgentState):

        task = state["messages"][-1].content
        prompt = PLANNER_PROMPT.invoke({
            "task": task
        })

        response = llm.invoke(prompt)

        print("\n===== RAW LLM OUTPUT =====")
        print(response.content)

        try:
            parsed = json.loads(response.content)
            state["steps"] = parsed["steps"]
        except Exception as e:
            print("Planner JSON parsing failed:", e)
            state["steps"] = []

        return state

    return _node
