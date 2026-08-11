import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    actor_id = Column(String(36), nullable=True)
    entity_type = Column(String(50), nullable=False)  # COMPANY, UNIT, ITEM, INVOICE, etc.
    entity_id = Column(String(36), nullable=False)
    action = Column(String(50), nullable=False)  # CREATED, UPDATED, DEACTIVATED, FINALIZED, etc.
    field_name = Column(String(100), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    company = relationship("Company", back_populates="audit_logs")
