from core.state import AgentState
from prompts.planner_prompt import PLANNER_PROMPT
import json

def planner(llm):
    def _node(state: AgentState):
        print("\n===== PLANNER STATE =====")
        print(state)
        print("=========================\n")

        task = state["messages"][-1].content
        prompt = PLANNER_PROMPT.invoke({
            "task": task
        })
        # prompt = PLANNER_PROMPT.invoke({
        #     "task": state["user_input"]
        # })

        response = llm.invoke(prompt)

        print("\n===== RAW LLM OUTPUT =====")
        print(response)
        print("==========================\n")

        # try:
        #     parsed = json.loads(response.content)
        #     state["steps"] = parsed["steps"]
        # except Exception as e:
        #     print("Planner JSON parsing failed:", e)
        #     state["steps"] = []

        # return state

    return _node
