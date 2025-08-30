from pydantic import BaseModel
from typing import Any

class MCPResponse(BaseModel):
    type: str
    request_id: str
    data: Any
