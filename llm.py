from langchain_ollama import ChatOllama


class LLM:
    def __init__(
        self,
        model: str = "qwen2.5:1.5b",
        # model: str = "qwen3.5:cloud",
        temperature: float = 0.0,
        # num_ctx: int = 1024,
        num_ctx=4096,
        top_p: float = 0.9,
        # num_predict: int = 516,
        num_predict=-1,
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
