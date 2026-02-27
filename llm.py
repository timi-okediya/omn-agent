from langchain_ollama import ChatOllama


class LLM:
    def __init__(
        self,
        model: str = "qwen3:1.7b",
        temperature: float = 0.2,
        num_ctx: int = 1024,
        top_p: float = 0.9,
        num_predict: int = 265,
        base_url: str = "http://172.23.16.1:11434",
    ):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            num_ctx=num_ctx,
            top_p=top_p,
            num_predict=num_predict,
            base_url=base_url,
        )

    def invoke(self, messages, **kwargs):
        return self.llm.invoke(messages, **kwargs)

    def bind_tools(self, tools):
        return self.llm.bind_tools(tools)
