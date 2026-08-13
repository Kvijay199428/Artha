from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.return_order import ReturnType, ReturnStatus, FinancialStatus, SettlementType, ItemCondition, WarehouseAction

class ReturnOrderLineCreate(BaseModel):
    original_order_line_id: str
    return_quantity: Decimal
    condition: Optional[ItemCondition] = ItemCondition.GOOD
    warehouse_action: Optional[WarehouseAction] = WarehouseAction.RETURN_TO_STOCK

class ReturnOrderCreate(BaseModel):
    original_order_id: str
    return_type: ReturnType
    reason: Optional[str] = None
    lines: List[ReturnOrderLineCreate]

class ReturnOrderLineResponse(BaseModel):
    id: str
    original_order_line_id: str
    item_id: Optional[str]
    item_name_snapshot: str
    sku_snapshot: Optional[str]
    hsn_sac_snapshot: Optional[str]
    unit_snapshot: Optional[str]
    
    original_quantity: float
    previously_returned_quantity: float
    return_quantity: float
    remaining_quantity: float
    
    rate: float
    taxable_value: float
    gst_rate: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    line_total: float
    
    condition: str
    warehouse_action: str

class ReturnSettlementResponse(BaseModel):
    id: str
    settlement_type: str
    amount: float
    status: str
    settlement_date: datetime
    reference_number: Optional[str]
    notes: Optional[str]

class ReturnOrderResponse(BaseModel):
    id: str
    return_number: Optional[str]
    return_type: str
    original_order_id: str
    party_id: str
    return_date: date
    
    status: str
    financial_status: str
    reason: Optional[str]
    
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    
    created_at: datetime
    lines: List[ReturnOrderLineResponse]
    settlements: List[ReturnSettlementResponse]

class ReturnOrderListResponse(BaseModel):
    items: List[ReturnOrderResponse]
    total: int

class ReturnableLineResponse(BaseModel):
    original_order_line_id: str
    item_name_snapshot: str
    unit_symbol_snapshot: Optional[str]
    rate: float
    gst_rate: float
    original_quantity: float
    previously_returned_quantity: float
    returnable_quantity: float

class ReturnableLinesResponse(BaseModel):
    order_id: str
    order_type: str
    tax_treatment: str
    lines: List[ReturnableLineResponse]

class ReturnSettlementCreate(BaseModel):
    settlement_type: SettlementType
    amount: Decimal
    reference_number: Optional[str] = None
    notes: Optional[str] = None
