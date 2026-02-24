from typing import Literal, Optional, Dict
from pydantic import BaseModel

class ToolResponse(BaseModel):
    status: Literal["success", "failure", "error"]
    message: str
    data: Optional[Dict] = None
