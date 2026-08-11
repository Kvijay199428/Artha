from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UnitCreate(BaseModel):
    unit_name: str = Field(..., min_length=1, max_length=100)
    symbol: str = Field(..., min_length=1, max_length=20)
    internal_code: Optional[str] = Field(None, max_length=20)
    gst_unit_code: Optional[str] = Field(None, max_length=20)
    category_id: Optional[str] = None
    unit_type: str = Field(default="CUSTOM")
    base_unit_id: Optional[str] = None
    conversion_factor: Optional[float] = None
    conversion_formula: Optional[str] = Field(None, max_length=500)
    precision: int = Field(default=2, ge=0, le=8)
    rounding_mode: str = Field(default="HALF_UP")

class UnitResponse(BaseModel):
    id: str
    company_id: str
    unit_name: str
    symbol: str
    internal_code: Optional[str]
    gst_unit_code: Optional[str]
    unit_type: str
    base_unit_id: Optional[str]
    conversion_factor: Optional[float]
    conversion_formula: Optional[str]
    precision: int
    is_predefined: bool
    is_active: bool
    created_at: datetime

class UnitListResponse(BaseModel):
    items: list[UnitResponse]
