from pydantic import BaseModel
from typing import Literal, Optional

class ErrorResponse(BaseModel):
    type: Literal["error"]
    request_id: Optional[str]
    error: str