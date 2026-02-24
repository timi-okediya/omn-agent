from langchain_core.tools import tool

@tool
def ping_server() -> str:
    """Use this tool ONLY when the user wants to check if the server is alive."""
    return "Server is dead"
