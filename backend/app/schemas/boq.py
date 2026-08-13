from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.boq import BOQStatus, BOQItemType

class BOQLineCreate(BaseModel):
    parent_line_id: Optional[str] = None
    section: Optional[str] = None
    item_type: BOQItemType = BOQItemType.MATERIAL
    item_id: Optional[str] = None
    description: str
    specification: Optional[str] = None
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    quantity_formula: Optional[str] = None
    estimated_rate: Optional[Decimal] = Decimal('0')
    remarks: Optional[str] = None
    sort_order: int = 0

class BOQCreate(BaseModel):
    project_name: Optional[str] = None
    party_id: Optional[str] = None
    boq_date: datetime
    notes: Optional[str] = None
    lines: List[BOQLineCreate]

class BOQLineResponse(BaseModel):
    id: str
    parent_line_id: Optional[str]
    section: Optional[str]
    item_type: str
    item_id: Optional[str]
    description: str
    specification: Optional[str]
    quantity: float
    unit_id: Optional[str]
    unit_snapshot: Optional[str]
    quantity_formula: Optional[str]
    estimated_rate: float
    estimated_amount: float
    remarks: Optional[str]
    sort_order: int

class BOQResponse(BaseModel):
    id: str
    boq_number: Optional[str]
    project_name: Optional[str]
    party_id: Optional[str]
    boq_date: datetime
    version: int
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    lines: List[BOQLineResponse]

class BOQListResponse(BaseModel):
    items: List[BOQResponse]
    total: int
