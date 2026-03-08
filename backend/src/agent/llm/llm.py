import os
from langchain_ollama import ChatOllama
from tools import TOOLS


class LLM:
    def __init__(
        self,
        model: str = None,
        temperature: float = 0.0,
        num_ctx: int = 4096,
        top_p: float = 0.9,
        num_predict: int = -1,
        base_url: str = None,
        bind_tools: bool = False,
    ):
        model = model or os.getenv("LLM_MODEL", "qwen2.5:3b")
        base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://172.23.16.1:11434")

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
        self.llm = self.llm.bind_tools(TOOLS)
        return self
