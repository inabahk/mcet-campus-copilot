from pydantic import BaseModel
from typing import Optional, List

class CopilotRequest(BaseModel):
    goal: str
    agent: str = "auto"
    context: Optional[str] = ""

class CopilotResponse(BaseModel):
    agent: str
    trace: List[str]
    title: str
    result: str
