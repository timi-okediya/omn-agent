from core import AgentState, PlanStep
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
        # print(response.content)
        print(response)

        try:
            parsed = json.loads(response.content)

            steps = [
                PlanStep(action=step["action"])
                for step in parsed.get("steps", [])
            ]

            return {
                "plan": steps,
                "current_step": 0,   # reset step counter
            }

        except Exception as e:
            print("Planner JSON parsing failed:", e)

            return {
                "plan": [],
                "current_step": 0,
            }

    return _node
