from .ping import ping_server
from .FileToolManager import FILE_TOOLS
from .GitToolManager import GIT_TOOLS

TOOLS = [
    ping_server,
    *FILE_TOOLS,
    *GIT_TOOLS,
]
