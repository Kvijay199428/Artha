import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Item(Base):
    __tablename__ = "items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    item_type = Column(String(20), nullable=False)  # PRODUCT, SERVICE
    item_name = Column(String(200), nullable=False)
    sku_code = Column(String(100), nullable=True)
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    hsn_sac_code = Column(String(20), nullable=True)
    gst_applicable = Column(Boolean, default=True)
    default_gst_rate_id = Column(String(36), ForeignKey("gst_rates.id"), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, INACTIVE, ARCHIVED
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    version = Column(Integer, default=1)
    
    versions = relationship("ItemVersion", back_populates="item", cascade="all, delete-orphan")

class ItemVersion(Base):
    __tablename__ = "item_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    item_name = Column(String(200), nullable=True)
    unit_id = Column(String(36), nullable=True)
    sku_code = Column(String(100), nullable=True)
    hsn_sac_code = Column(String(20), nullable=True)
    gst_rate_id = Column(String(36), nullable=True)
    description = Column(Text, nullable=True)
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    item = relationship("Item", back_populates="versions")
