import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class DocumentLink(Base):
    __tablename__ = "document_links"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    source_type = Column(String(50), nullable=False)
    source_id = Column(String(36), nullable=False)
    source_revision = Column(Integer, nullable=True)
    
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False)
    target_revision = Column(Integer, nullable=True)
    
    relationship_type = Column(String(50), nullable=False) # e.g. "ESTIMATED_FROM_BOQ", "QUOTED_FROM_ESTIMATE", "CONVERTED_TO_ORDER"
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)

class BOQStatus(enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PRICED = "PRICED"
    FINALIZED = "FINALIZED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"

class BOQItemType(enum.Enum):
    MATERIAL = "MATERIAL"
    LABOUR = "LABOUR"
    SERVICE = "SERVICE"
    EQUIPMENT = "EQUIPMENT"
    SUBCONTRACT = "SUBCONTRACT"
    OTHER = "OTHER"

class BOQ(Base):
    __tablename__ = "boqs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    boq_number = Column(String(50), nullable=True)
    project_name = Column(String(200), nullable=True)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    
    boq_date = Column(DateTime, nullable=False, default=utc_now)
    version = Column(Integer, default=1)
    status = Column(Enum(BOQStatus), default=BOQStatus.DRAFT)
    
    notes = Column(Text, nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("BOQLine", back_populates="boq", cascade="all, delete-orphan")

class BOQLine(Base):
    __tablename__ = "boq_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    boq_id = Column(String(36), ForeignKey("boqs.id"), nullable=False)
    
    parent_line_id = Column(String(36), ForeignKey("boq_lines.id"), nullable=True)
    
    section = Column(String(100), nullable=True)
    item_type = Column(Enum(BOQItemType), default=BOQItemType.MATERIAL)
    
    item_id = Column(String(36), nullable=True)
    description = Column(String(255), nullable=False)
    specification = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    quantity_formula = Column(String(255), nullable=True)
    
    estimated_rate = Column(Numeric(15, 4), default=0)
    estimated_amount = Column(Numeric(15, 2), default=0)
    
    remarks = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0)
    
    boq = relationship("BOQ", back_populates="lines")
    children = relationship("BOQLine")
