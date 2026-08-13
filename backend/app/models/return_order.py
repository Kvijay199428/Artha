import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class ReturnType(enum.Enum):
    SUPPLY_IN_RETURN = "SUPPLY_IN_RETURN"
    SUPPLY_OUT_RETURN = "SUPPLY_OUT_RETURN"

class ReturnStatus(enum.Enum):
    DRAFT = "DRAFT"
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class FinancialStatus(enum.Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    ADJUSTED = "ADJUSTED"
    REFUND_PENDING = "REFUND_PENDING"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    REFUNDED = "REFUNDED"
    CREDIT_CREATED = "CREDIT_CREATED"

class SettlementType(enum.Enum):
    ADJUST_RECEIVABLE = "ADJUST_RECEIVABLE"
    ADJUST_PAYABLE = "ADJUST_PAYABLE"
    CUSTOMER_REFUND = "CUSTOMER_REFUND"
    SUPPLIER_REFUND = "SUPPLIER_REFUND"
    CUSTOMER_CREDIT = "CUSTOMER_CREDIT"
    SUPPLIER_CREDIT = "SUPPLIER_CREDIT"

class ItemCondition(enum.Enum):
    GOOD = "GOOD"
    DAMAGED = "DAMAGED"
    DEFECTIVE = "DEFECTIVE"
    EXPIRED = "EXPIRED"
    REPAIR = "REPAIR"
    SCRAP = "SCRAP"
    OTHER = "OTHER"

class WarehouseAction(enum.Enum):
    RETURN_TO_STOCK = "RETURN_TO_STOCK"
    QUARANTINE = "QUARANTINE"
    REPAIR = "REPAIR"
    SCRAP = "SCRAP"
    RETURN_TO_SUPPLIER = "RETURN_TO_SUPPLIER"
    NONE = "NONE"

class ReturnOrder(Base):
    __tablename__ = "returns"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    return_number = Column(String(50), nullable=True)
    return_type = Column(Enum(ReturnType), nullable=False)
    
    original_order_id = Column(String(36), ForeignKey("supply_orders.id"), nullable=False)
    original_order_type = Column(String(20), nullable=False)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    return_date = Column(DateTime, nullable=False, default=utc_now)
    
    status = Column(Enum(ReturnStatus), default=ReturnStatus.DRAFT)
    financial_status = Column(Enum(FinancialStatus), default=FinancialStatus.NOT_REQUIRED)
    
    reason = Column(Text, nullable=True)
    
    # Financial Totals
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
    
    created_by = Column(String(36), nullable=True)
    approved_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("ReturnOrderLine", back_populates="return_order", cascade="all, delete-orphan")
    settlements = relationship("ReturnSettlement", back_populates="return_order", cascade="all, delete-orphan")

class ReturnOrderLine(Base):
    __tablename__ = "return_lines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    return_id = Column(String(36), ForeignKey("returns.id"), nullable=False)
    original_order_line_id = Column(String(36), ForeignKey("supply_order_lines.id"), nullable=False)
    item_id = Column(String(36), nullable=True)
    
    # Snapshots from original
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    # Quantities
    original_quantity = Column(Numeric(15, 5), nullable=False)
    previously_returned_quantity = Column(Numeric(15, 5), default=0)
    return_quantity = Column(Numeric(15, 5), nullable=False)
    remaining_quantity = Column(Numeric(15, 5), nullable=False)
    
    # Financials (snapshots from original)
    original_rate = Column(Numeric(15, 4), nullable=False)
    rate = Column(Numeric(15, 4), nullable=False)
    
    discount_type = Column(String(20), nullable=True)
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(String(20), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), default=0)
    
    # Condition
    condition = Column(Enum(ItemCondition), default=ItemCondition.GOOD)
    warehouse_action = Column(Enum(WarehouseAction), default=WarehouseAction.RETURN_TO_STOCK)
    
    return_order = relationship("ReturnOrder", back_populates="lines")

class ReturnSettlement(Base):
    __tablename__ = "return_settlements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    return_id = Column(String(36), ForeignKey("returns.id"), nullable=False)
    
    settlement_type = Column(Enum(SettlementType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    payment_id = Column(String(36), nullable=True) # Linked to a Payment if it's a direct refund
    ledger_entry_id = Column(String(36), nullable=True)
    
    status = Column(String(20), default="COMPLETED")
    settlement_date = Column(DateTime, nullable=False, default=utc_now)
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    
    return_order = relationship("ReturnOrder", back_populates="settlements")
