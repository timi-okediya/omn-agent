from .ping import ping_server
from .FileToolManager import FILE_TOOLS

TOOLS = [
    ping_server,
    *FILE_TOOLS
]
