from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.estimate import EstimateStatus

class EstimateLineCreate(BaseModel):
    item_name_snapshot: str
    item_type: Optional[str] = None
    quantity: Decimal
    unit_snapshot: Optional[str] = None
    cost_rate: Optional[Decimal] = Decimal('0')
    markup_percent: Optional[Decimal] = Decimal('0')

class EstimateCreate(BaseModel):
    boq_id: Optional[str] = None
    party_id: Optional[str] = None
    estimate_date: datetime
    valid_until: Optional[datetime] = None
    lines: List[EstimateLineCreate]

class EstimateLineResponse(BaseModel):
    id: str
    item_name_snapshot: str
    item_type: Optional[str]
    quantity: float
    unit_snapshot: Optional[str]
    cost_rate: float
    cost_amount: float
    markup_percent: float
    markup_amount: float
    selling_rate: float
    selling_amount: float

class EstimateResponse(BaseModel):
    id: str
    estimate_number: Optional[str]
    boq_id: Optional[str]
    party_id: Optional[str]
    estimate_date: datetime
    valid_until: Optional[datetime]
    version: int
    status: str
    material_cost: float
    labour_cost: float
    service_cost: float
    other_cost: float
    total_cost: float
    markup_amount: float
    estimated_selling_value: float
    gst_total: float
    grand_total: float
    created_at: datetime
    updated_at: datetime
    lines: List[EstimateLineResponse]

class EstimateListResponse(BaseModel):
    items: List[EstimateResponse]
    total: int
