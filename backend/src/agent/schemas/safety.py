from pydantic import BaseModel, Field

class SafetyCheck(BaseModel):
    is_safe: bool = Field(
        description="True if the request is safe. False if it is unsafe."
    )
    reason: str
