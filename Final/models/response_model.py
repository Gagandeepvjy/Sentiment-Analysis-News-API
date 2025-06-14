from pydantic import BaseModel
from typing import Any, Optional
class ResponseBaseModel(BaseModel):
    data: Any
    error: Optional[str]
    message: Optional[str]
    status_code: int