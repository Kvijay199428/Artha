import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class EstimateStatus(enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    CONVERTED_TO_QUOTATION = "CONVERTED_TO_QUOTATION"

class Estimate(Base):
    __tablename__ = "estimates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    estimate_number = Column(String(50), nullable=True)
    boq_id = Column(String(36), ForeignKey("boqs.id"), nullable=True)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    
    estimate_date = Column(DateTime, nullable=False, default=utc_now)
    valid_until = Column(DateTime, nullable=True)
    
    version = Column(Integer, default=1)
    status = Column(Enum(EstimateStatus), default=EstimateStatus.DRAFT)
    
    material_cost = Column(Numeric(15, 2), default=0)
    labour_cost = Column(Numeric(15, 2), default=0)
    service_cost = Column(Numeric(15, 2), default=0)
    other_cost = Column(Numeric(15, 2), default=0)
    
    total_cost = Column(Numeric(15, 2), default=0)
    markup_amount = Column(Numeric(15, 2), default=0)
    estimated_selling_value = Column(Numeric(15, 2), default=0)
    
    gst_total = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("EstimateLine", back_populates="estimate", cascade="all, delete-orphan")

class EstimateLine(Base):
    __tablename__ = "estimate_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    estimate_id = Column(String(36), ForeignKey("estimates.id"), nullable=False)
    
    item_name_snapshot = Column(String(255), nullable=False)
    item_type = Column(String(50), nullable=True) # Matches BOQItemType
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_snapshot = Column(String(50), nullable=True)
    
    cost_rate = Column(Numeric(15, 4), default=0)
    cost_amount = Column(Numeric(15, 2), default=0)
    
    markup_percent = Column(Numeric(5, 2), default=0)
    markup_amount = Column(Numeric(15, 2), default=0)
    
    selling_rate = Column(Numeric(15, 4), default=0)
    selling_amount = Column(Numeric(15, 2), default=0)
    
    estimate = relationship("Estimate", back_populates="lines")
