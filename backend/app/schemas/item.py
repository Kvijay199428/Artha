from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    item_type: str = Field(..., pattern="^(PRODUCT|SERVICE)$")
    item_name: str = Field(..., min_length=1, max_length=200)
    unit_id: str = Field(...)
    sku_code: Optional[str] = Field(None, max_length=100)
    hsn_sac_code: Optional[str] = Field(None, max_length=20)
    gst_applicable: bool = True
    gst_rate_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)

class ItemUpdate(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=200)
    unit_id: Optional[str] = None
    sku_code: Optional[str] = Field(None, max_length=100)
    hsn_sac_code: Optional[str] = Field(None, max_length=20)
    gst_applicable: Optional[bool] = None
    gst_rate_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE|ARCHIVED)$")

class ItemResponse(BaseModel):
    id: str
    company_id: str
    item_type: str
    item_name: str
    sku_code: Optional[str]
    unit_id: str
    unit_name: Optional[str]
    unit_symbol: Optional[str]
    hsn_sac_code: Optional[str]
    gst_applicable: bool
    gst_rate_id: Optional[str]
    gst_rate: Optional[float]
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class ItemListResponse(BaseModel):
    items: list[ItemResponse]
