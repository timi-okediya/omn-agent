from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

from core.state import AgentState
from nodes import safety_check, planner, executor, review, reflection
from llm import LLM
from tools import TOOLS


planner_llm = LLM()
executor_llm = LLM(bind_tools=True)


def executor_router(state: AgentState):
    plan = state.get("plan") or []
    current_step = state.get("current_step", 0)
    messages = state.get("messages", [])

    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tools"
    if current_step < len(plan):
        return "executor"
    return "reflection"


def reflection_router(state: AgentState):
    if state.get("reflection_passed"):
        return "review"
    if state.get("retry_count", 0) >= 3:
        return "review"
    return "executor"


def review_router(state: AgentState):
    if state.get("review_passed"):
        return END
    if state.get("retry_count", 0) >= 3:
        return END
    return "executor"


workflow = StateGraph(AgentState)

workflow.add_node("safety_check", safety_check(planner_llm))
workflow.add_node("planner", planner(planner_llm))
workflow.add_node("executor", executor(executor_llm))
workflow.add_node("tools", ToolNode(TOOLS))
workflow.add_node("reflection", reflection(planner_llm))
workflow.add_node("review", review(planner_llm))

workflow.add_edge(START, "safety_check")

workflow.add_conditional_edges(
    "safety_check",
    lambda state: "planner" if state.get("safety_passed") else END,
)

workflow.add_edge("planner", "executor")
workflow.add_conditional_edges("executor", executor_router)
workflow.add_edge("tools", "executor")
workflow.add_conditional_edges("reflection", reflection_router)
workflow.add_conditional_edges("review", review_router)

app = workflow.compile()
