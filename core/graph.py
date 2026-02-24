from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode, tools_condition

from core.state import AgentState
from llm import LLM
from tools import TOOLS

llm = LLM()


def assistant(state: AgentState):
    response = llm.invoke(state["messages"])
    return {"messages": state["messages"] + [response]}


workflow = StateGraph(AgentState)

workflow.add_node("assistant", assistant)
workflow.add_node("tools", ToolNode(TOOLS))

workflow.add_conditional_edges(
    "assistant",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END,
    },
)

workflow.add_edge("tools", "assistant")
workflow.add_edge(START, "assistant")

app = workflow.compile()

