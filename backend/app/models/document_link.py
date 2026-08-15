import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class DocumentLink(Base):
    __tablename__ = "document_links"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    source_type = Column(String(50), nullable=False)
    source_id = Column(String(36), nullable=False)
    source_number = Column(String(100), nullable=True)
    source_revision = Column(Integer, nullable=True)
    
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False)
    target_number = Column(String(100), nullable=True)
    target_revision = Column(Integer, nullable=True)
    
    relationship_type = Column(String(50), nullable=False)
    
    quantity = Column(Numeric(15, 5), nullable=True)
    amount = Column(Numeric(15, 2), nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)


class DocumentLineLink(Base):
    __tablename__ = "document_line_links"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    source_document_type = Column(String(50), nullable=False)
    source_document_id = Column(String(36), nullable=False)
    source_line_id = Column(String(36), nullable=False)
    
    target_document_type = Column(String(50), nullable=False)
    target_document_id = Column(String(36), nullable=False)
    target_line_id = Column(String(36), nullable=False)
    
    source_quantity = Column(Numeric(15, 5), nullable=True)
    converted_quantity = Column(Numeric(15, 5), nullable=True)
    
    source_amount = Column(Numeric(15, 2), nullable=True)
    converted_amount = Column(Numeric(15, 2), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
