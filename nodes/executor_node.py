from core import AgentState
from llm import LLM


def executor_node(llm: LLM):
    def _node(state: AgentState):
        print(state)

        return state
    return _node
