import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    invoice_series = Column(String(50), nullable=False)
    invoice_type = Column(String(30), default="TAX_INVOICE")
    invoice_date = Column(DateTime, nullable=False)
    accounting_period_id = Column(String(36), nullable=True)
    
    order_id = Column(String(36), ForeignKey("supply_orders.id"), nullable=True)
    transaction_type = Column(String(20), default="SALES") # SALES or PURCHASE
    
    # Customer snapshots (For SALES, this is the party. For PURCHASE, this is the company)
    customer_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    customer_name_snapshot = Column(String(200), nullable=False)
    customer_gstin_snapshot = Column(String(15), nullable=True)
    customer_address_snapshot = Column(Text, nullable=True)
    customer_state_snapshot = Column(String(100), nullable=True)
    customer_state_code_snapshot = Column(String(2), nullable=True)
    place_of_supply = Column(String(100), nullable=False)
    
    # Seller snapshots (For SALES, this is the company. For PURCHASE, this is the party)
    shipping_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    
    financial_year = Column(String(20), nullable=True)
    
    # Pre-invoice genealogy fields
    origin_document_type = Column(String(50), nullable=True)
    origin_document_id = Column(String(36), nullable=True)
    origin_document_number = Column(String(100), nullable=True)
    
    source_order_id = Column(String(36), nullable=True)
    source_order_number = Column(String(100), nullable=True)
    seller_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    seller_name_snapshot = Column(String(200), nullable=False)
    seller_gstin_snapshot = Column(String(15), nullable=True)
    seller_address_snapshot = Column(Text, nullable=True)
    seller_state_snapshot = Column(String(100), nullable=True)
    seller_state_code_snapshot = Column(String(2), nullable=True)
    
    currency_code = Column(String(3), default="INR")
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    other_charges = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(500), nullable=True)
    
    invoice_status = Column(String(20), default="DRAFT")  # DRAFT, FINALIZED, CANCELLED, VOID
    payment_status = Column(String(20), default="UNPAID")  # UNPAID, PARTIALLY_PAID, PAID
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    finalized_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1)
    
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    item_id = Column(String(36), nullable=True)
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    description_snapshot = Column(Text, nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_name_snapshot = Column(String(50), nullable=True)
    unit_symbol_snapshot = Column(String(20), nullable=True)
    conversion_factor = Column(Numeric(15, 5), default=1)
    base_quantity = Column(Numeric(15, 5), nullable=True)
    
    rate = Column(Numeric(15, 4), nullable=False)
    discount_type = Column(String(20), nullable=True)  # NONE, PERCENT, FIXED
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    taxable_value = Column(Numeric(15, 2), default=0)
    
    gst_rate = Column(Numeric(5, 2), default=0)
    cgst_rate = Column(Numeric(5, 2), default=0)
    sgst_rate = Column(Numeric(5, 2), default=0)
    igst_rate = Column(Numeric(5, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    line_total = Column(Numeric(15, 2), default=0)
    
    invoice = relationship("Invoice", back_populates="lines")

class InvoiceSeries(Base):
    __tablename__ = "invoice_series"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    document_type = Column(String(30), default="TAX_INVOICE")
    prefix = Column(String(50), nullable=False)
    suffix = Column(String(50), nullable=True)
    starting_number = Column(Integer, default=1)
    current_number = Column(Integer, default=1)
    fiscal_year = Column(String(20), nullable=True)
    reset_policy = Column(String(20), default="NEVER")  # NEVER, YEARLY
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=utc_now)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=True)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_mode = Column(String(30), nullable=False)  # CASH, BANK_TRANSFER, UPI, CARD, CHEQUE, NEFT, RTGS, IMPS
    reference_number = Column(String(100), nullable=True)
    bank_account_id = Column(String(36), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="COMPLETED")
    created_at = Column(DateTime, default=utc_now)

