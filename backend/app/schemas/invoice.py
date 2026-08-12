from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class InvoiceLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    hsn_sac: Optional[str] = Field(None, max_length=20)
    quantity: float = Field(..., gt=0)
    unit_id: str = Field(...)
    unit_name: str = Field(...)
    unit_symbol: str = Field(...)
    rate: float = Field(..., ge=0)
    discount_type: str = Field(default="NONE")
    discount_value: float = Field(default=0, ge=0)
    gst_rate: float = Field(default=0, ge=0)

class InvoiceCreate(BaseModel):
    invoice_type: str = Field(default="TAX_INVOICE")
    invoice_date: date = Field(...)
    customer_id: str = Field(...)
    place_of_supply: str = Field(...)
    lines: list[InvoiceLineCreate] = Field(..., min_length=1)
    notes: Optional[str] = None
    terms: Optional[str] = None

class InvoiceCalculateRequest(BaseModel):
    customer_id: Optional[str] = None
    place_of_supply: str = Field(...)
    lines: list[InvoiceLineCreate] = Field(..., min_length=1)

class InvoiceCalculateResponse(BaseModel):
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    amount_in_words: Optional[str]
    lines: list[dict] # We can just return lines as dictionaries

class InvoiceLineResponse(BaseModel):
    id: str
    item_name: str
    description: Optional[str]
    hsn_sac_snapshot: Optional[str]
    quantity: float
    unit_name_snapshot: Optional[str]
    unit_symbol_snapshot: Optional[str]
    rate: float
    discount_amount: float
    taxable_value: float
    gst_rate: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    line_total: float

class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    invoice_type: str
    invoice_date: date
    customer_name_snapshot: str
    customer_gstin_snapshot: Optional[str]
    place_of_supply: str
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    amount_in_words: Optional[str]
    invoice_status: str
    payment_status: str
    notes: Optional[str]
    lines: list[InvoiceLineResponse]
    created_at: datetime

class InvoiceListResponse(BaseModel):
    items: list[InvoiceResponse]
    total: int

class InvoiceFinalizeRequest(BaseModel):
    pass  # Optionally add specific finalization flags if needed in future

class InvoiceCancelRequest(BaseModel):
    cancel_reason: str = Field(..., min_length=5, max_length=500)
