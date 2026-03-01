from langchain_ollama import ChatOllama
from tools import TOOLS


class LLM:
    def __init__(
        self,
        model: str = "qwen2.5:3b",
        temperature: float = 0.0,
        num_ctx: int = 4096,
        top_p: float = 0.9,
        num_predict: int = -1,
        base_url: str = "http://172.23.16.1:11434",
        bind_tools: bool = False,   # ← opt-in, off by default
    ):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            num_ctx=num_ctx,
            top_p=top_p,
            num_predict=num_predict,
            base_url=base_url,
        )

        if bind_tools:
            self.llm = self.llm.bind_tools(TOOLS)

    def invoke(self, messages, **kwargs):
        return self.llm.invoke(messages, **kwargs)

    def with_tools(self):
        """Return a new LLM instance with tools bound."""
        self.llm = self.llm.bind_tools(TOOLS)
        return self
