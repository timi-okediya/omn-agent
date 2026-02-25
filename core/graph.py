from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from core.nodes import executor, planner, review
from core.state import AgentState
from nodes import safety_check
from llm import LLM
from tools import TOOLS


# Base LLM
base_llm = LLM()

# Separate roles
planner_llm = base_llm
executor_llm = base_llm.bind_tools(TOOLS)


workflow = StateGraph(AgentState)

# nodes
workflow.add_node("safety_check", safety_check(planner_llm))
# workflow.add_node("planner", planner(planner_llm))
# workflow.add_node("executor", executor(executor_llm))
# workflow.add_node("review", review(planner_llm))
workflow.add_node("tools", ToolNode(TOOLS))


# START → safety
workflow.add_edge(START, "safety_check")

# # safety → planner OR END
# workflow.add_conditional_edges(
#     "safety_check",
#     lambda state: "planner" if state["safety_passed"] else END,
# )

# # planner → executor
# workflow.add_edge("planner", "executor")


# # Routing
# def executor_router(state: AgentState):

#     # Tool call?
#     if tools_condition(state) == "tools":
#         return "tools"

#     # More steps remaining?
#     if state["current_step"] < len(state["plan"]):
#         return "executor"

#     # Otherwise done
#     return "review"


# workflow.add_conditional_edges("executor", executor_router)

# # tools → executor (loop)
# workflow.add_edge("tools", "executor")

# # review → END
# workflow.add_edge("review", END)

app = workflow.compile()
