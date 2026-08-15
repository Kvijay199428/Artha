import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class AdjustmentNote(Base):
    __tablename__ = "adjustment_notes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    note_number = Column(String(50), nullable=False)
    note_type = Column(String(20), nullable=False) # CREDIT_NOTE, DEBIT_NOTE
    
    source_type = Column(String(50), nullable=True)
    source_id = Column(String(36), nullable=True)
    source_number = Column(String(50), nullable=True)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    party_role = Column(String(20), nullable=False) # CUSTOMER, SUPPLIER
    
    note_date = Column(DateTime, nullable=False)
    reason_code = Column(String(50), nullable=False)
    reason_description = Column(String(200), nullable=True)
    
    tax_treatment = Column(String(20), nullable=False) # GST, WITHOUT_GST
    gst_document = Column(Boolean, default=True)
    is_accounting_only = Column(Boolean, default=False)
    
    place_of_supply = Column(String(100), nullable=True)
    reverse_charge = Column(Boolean, default=False)
    
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    
    status = Column(String(20), default="DRAFT") # DRAFT, APPROVED, POSTED, CANCELLED, REJECTED
    
    created_by = Column(String(36), nullable=True)
    approved_by = Column(String(36), nullable=True)
    posted_by = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    posted_at = Column(DateTime, nullable=True)
    
    lines = relationship("AdjustmentNoteLine", back_populates="adjustment_note", cascade="all, delete-orphan")
    allocations = relationship("NoteAllocation", back_populates="adjustment_note", cascade="all, delete-orphan")


class AdjustmentNoteLine(Base):
    __tablename__ = "adjustment_note_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    adjustment_note_id = Column(String(36), ForeignKey("adjustment_notes.id"), nullable=False)
    
    source_line_id = Column(String(36), nullable=True)
    item_id = Column(String(36), nullable=True)
    
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    description = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    rate = Column(Numeric(15, 4), nullable=False)
    
    discount_type = Column(String(20), nullable=True)
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(String(20), nullable=True)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), default=0)
    
    adjustment_note = relationship("AdjustmentNote", back_populates="lines")


class NoteAllocation(Base):
    __tablename__ = "note_allocations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_id = Column(String(36), ForeignKey("adjustment_notes.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False)
    
    allocated_amount = Column(Numeric(15, 2), nullable=False)
    allocation_date = Column(DateTime, nullable=False)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    adjustment_note = relationship("AdjustmentNote", back_populates="allocations")
