import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class QuotationType(enum.Enum):
    SALES = "SALES"
    PURCHASE = "PURCHASE"

class QuotationStatus(enum.Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    SENT = "SENT"
    VIEWED = "VIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    WITHDRAWN = "WITHDRAWN"

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    quotation_number = Column(String(50), nullable=True)
    quotation_type = Column(Enum(QuotationType), nullable=False)
    tax_treatment = Column(String(20), nullable=False)
    
    quotation_date = Column(DateTime, nullable=False, default=utc_now)
    valid_until = Column(DateTime, nullable=False)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    status = Column(Enum(QuotationStatus), default=QuotationStatus.DRAFT)
    revision = Column(Integer, default=1)
    
    source_boq_id = Column(String(36), nullable=True)
    source_estimate_id = Column(String(36), nullable=True)
    
    place_of_supply = Column(String(100), nullable=False)
    
    # Financial Totals
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(500), nullable=True)
    
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    
    accepted_at = Column(DateTime, nullable=True)
    accepted_by = Column(String(36), nullable=True)
    acceptance_method = Column(String(50), nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    # Conversion Tracking
    converted_quantity_total = Column(Numeric(15, 5), default=0)
    fully_converted = Column(Boolean, default=False)
    
    lines = relationship("QuotationLine", back_populates="quotation", cascade="all, delete-orphan")

class QuotationLine(Base):
    __tablename__ = "quotation_lines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quotation_id = Column(String(36), ForeignKey("quotations.id"), nullable=False)
    
    item_id = Column(String(36), nullable=True)
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    converted_quantity = Column(Numeric(15, 5), default=0)
    
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
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
    
    quotation = relationship("Quotation", back_populates="lines")
