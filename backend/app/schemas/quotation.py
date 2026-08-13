from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.quotation import QuotationStatus, QuotationType

class QuotationLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name_snapshot: str
    description: Optional[str] = None
    hsn_sac_snapshot: Optional[str] = None
    sku_snapshot: Optional[str] = None
    
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    
    rate: Decimal
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = Decimal('0')
    gst_rate: Optional[Decimal] = Decimal('0')

class QuotationCreate(BaseModel):
    quotation_type: QuotationType
    tax_treatment: str
    party_id: str
    
    valid_until: datetime
    place_of_supply: str
    
    notes: Optional[str] = None
    terms: Optional[str] = None
    
    lines: List[QuotationLineCreate]

class QuotationLineResponse(BaseModel):
    id: str
    item_id: Optional[str]
    item_name_snapshot: str
    description: Optional[str]
    hsn_sac_snapshot: Optional[str]
    sku_snapshot: Optional[str]
    
    quantity: float
    converted_quantity: float
    unit_id: Optional[str]
    unit_snapshot: Optional[str]
    
    rate: float
    discount_type: Optional[str]
    discount_value: float
    discount_amount: float
    
    tax_treatment: str
    gst_rate: float
    
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: float
    
    line_total: float

class QuotationResponse(BaseModel):
    id: str
    quotation_number: Optional[str]
    quotation_type: str
    tax_treatment: str
    party_id: str
    
    quotation_date: datetime
    valid_until: datetime
    
    status: str
    revision: int
    
    place_of_supply: str
    
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    round_off: float
    grand_total: float
    
    notes: Optional[str]
    terms: Optional[str]
    
    accepted_at: Optional[datetime]
    accepted_by: Optional[str]
    acceptance_method: Optional[str]
    
    fully_converted: bool
    
    created_at: datetime
    
    lines: List[QuotationLineResponse]

class QuotationListResponse(BaseModel):
    items: List[QuotationResponse]
    total: int

class QuotationAcceptRequest(BaseModel):
    acceptance_method: str = "USER_ACCEPTED"
