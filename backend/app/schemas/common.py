from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: Optional[dict] = None
