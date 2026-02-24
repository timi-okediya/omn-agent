from langchain_ollama import ChatOllama

from tools import TOOLS


class LLM:
    def __init__(
        self,
        # model: str = "qwen2.5:3b",
        # temperature: float = 0.0,
        # num_ctx: int = 2048,
        # top_p: float = 1.0,
        # num_predict: int = 256,
        model: str = "qwen2.5:1.5b",
        temperature: float = 0.2,
        num_ctx: int = 1024,
        top_p: float = 0.9,
        num_predict: int = 128,
    ):
        self.model = model
        self.temperature = temperature
        self.num_ctx = num_ctx
        self.top_p = top_p
        self.num_predict = num_predict

        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            num_ctx=num_ctx,
            top_p=top_p,
            num_predict=num_predict,
            base_url="http://172.23.16.1:11434"
        )
        self.llm = self.llm.bind_tools(TOOLS)

    def invoke(self, messages):
        return self.llm.invoke(messages)
