from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from app.models.order import OrderType, TaxTreatment, OrderStatus

class SupplyOrderLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name: str
    sku: Optional[str] = None
    hsn_sac: Optional[str] = None
    unit_id: str
    unit_name: str
    unit_symbol: str
    quantity: float
    rate: float
    discount_type: str = "NONE"
    discount_value: float = 0
    gst_rate: float = 0
    description: Optional[str] = None

class SupplyOrderCreate(BaseModel):
    order_type: OrderType
    tax_treatment: TaxTreatment
    party_id: str
    order_date: date
    expected_date: Optional[date] = None
    place_of_supply: str
    lines: List[SupplyOrderLineCreate] = Field(..., min_length=1)
    quotation_id: Optional[str] = None
    notes: Optional[str] = None
    terms: Optional[str] = None

class SupplyOrderCalculateRequest(BaseModel):
    tax_treatment: TaxTreatment
    party_id: Optional[str] = None
    place_of_supply: str
    lines: List[SupplyOrderLineCreate] = Field(..., min_length=1)

class SupplyOrderCalculateResponse(BaseModel):
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    grand_total: float
    amount_in_words: Optional[str]
    lines: List[dict]

class SupplyOrderLineResponse(BaseModel):
    id: str
    item_id: Optional[str]
    item_name_snapshot: str
    sku_snapshot: Optional[str]
    hsn_sac_snapshot: Optional[str]
    unit_id: str
    unit_name_snapshot: str
    unit_symbol_snapshot: str
    quantity: float
    fulfilled_quantity: float
    rate: float
    discount_type: str
    discount_value: float
    tax_treatment: str
    gst_rate: float
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: float
    line_total: float
    description: Optional[str]

class SupplyOrderResponse(BaseModel):
    id: str
    order_type: str
    tax_treatment: str
    order_number: Optional[str]
    order_date: date
    expected_date: Optional[date]
    party_id: str
    place_of_supply: str
    status: str
    revision: int
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    other_charges: float
    round_off: float
    grand_total: float
    amount_in_words: Optional[str]
    notes: Optional[str]
    terms: Optional[str]
    lines: List[SupplyOrderLineResponse]

class SupplyOrderListResponse(BaseModel):
    items: List[SupplyOrderResponse]
    total: int
