from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

class MCPRequest(BaseModel):
    type: Literal["list_tools", "call_tool"]
    request_id: str = Field(..., min_length=1)
    data: Optional[Any] = None
