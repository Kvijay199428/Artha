from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class AdjustmentNoteLineBase(BaseModel):
    source_line_id: Optional[str] = None
    item_id: Optional[str] = None
    item_name_snapshot: str
    sku_snapshot: Optional[str] = None
    hsn_sac_snapshot: Optional[str] = None
    description: Optional[str] = None
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    rate: Decimal
    discount_type: Optional[str] = None
    discount_value: Decimal = Decimal('0')
    discount_amount: Decimal = Decimal('0')
    tax_treatment: Optional[str] = None
    gst_rate: Decimal = Decimal('0')
    taxable_value: Decimal = Decimal('0')
    cgst_amount: Decimal = Decimal('0')
    sgst_amount: Decimal = Decimal('0')
    igst_amount: Decimal = Decimal('0')
    cess_amount: Decimal = Decimal('0')
    line_total: Decimal = Decimal('0')

class AdjustmentNoteLineCreate(AdjustmentNoteLineBase):
    pass

class AdjustmentNoteLineResponse(AdjustmentNoteLineBase):
    id: str
    adjustment_note_id: str

    class Config:
        from_attributes = True

class AdjustmentNoteBase(BaseModel):
    note_type: str
    source_type: Optional[str] = None
    source_id: Optional[str] = None
    source_number: Optional[str] = None
    party_id: str
    party_role: str
    note_date: datetime
    reason_code: str
    reason_description: Optional[str] = None
    tax_treatment: str
    gst_document: bool = True
    is_accounting_only: bool = False
    place_of_supply: Optional[str] = None
    reverse_charge: bool = False
    subtotal: Decimal = Decimal('0')
    discount_total: Decimal = Decimal('0')
    taxable_total: Decimal = Decimal('0')
    cgst_total: Decimal = Decimal('0')
    sgst_total: Decimal = Decimal('0')
    igst_total: Decimal = Decimal('0')
    cess_total: Decimal = Decimal('0')
    round_off: Decimal = Decimal('0')
    grand_total: Decimal = Decimal('0')

class AdjustmentNoteCreate(AdjustmentNoteBase):
    lines: List[AdjustmentNoteLineCreate]

class AdjustmentNoteResponse(AdjustmentNoteBase):
    id: str
    company_id: str
    note_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    posted_at: Optional[datetime] = None
    lines: List[AdjustmentNoteLineResponse] = []

    class Config:
        from_attributes = True

class NoteAllocationBase(BaseModel):
    target_type: str
    target_id: str
    allocated_amount: Decimal
    allocation_date: datetime

class NoteAllocationCreate(NoteAllocationBase):
    pass

class NoteAllocationResponse(NoteAllocationBase):
    id: str
    note_id: str
    party_id: str
    created_at: datetime

    class Config:
        from_attributes = True
