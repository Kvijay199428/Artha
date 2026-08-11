import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    unit_name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    internal_code = Column(String(20), nullable=True)
    gst_unit_code = Column(String(20), nullable=True)
    category_id = Column(String(36), ForeignKey("unit_categories.id"), nullable=True)
    unit_type = Column(String(20), default="BASE")  # BASE, DERIVED, COMPOUND, COUNT, COMMERCIAL, CUSTOM
    base_unit_id = Column(String(36), ForeignKey("units.id"), nullable=True)
    conversion_factor = Column(Numeric(20, 10), nullable=True)
    conversion_formula = Column(String(500), nullable=True)
    precision = Column(Integer, default=2)
    rounding_mode = Column(String(20), default="HALF_UP")
    is_predefined = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    aliases = relationship("UnitAlias", back_populates="unit", cascade="all, delete-orphan")
    versions = relationship("UnitVersion", back_populates="unit", cascade="all, delete-orphan")

class UnitCategory(Base):
    __tablename__ = "unit_categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    dimension = Column(String(50), nullable=True)
    status = Column(String(20), default="ACTIVE")

class UnitAlias(Base):
    __tablename__ = "unit_aliases"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    alias = Column(String(50), nullable=False)
    normalized_alias = Column(String(50), nullable=False)
    
    unit = relationship("Unit", back_populates="aliases")

class UnitVersion(Base):
    __tablename__ = "unit_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    conversion_formula = Column(String(500), nullable=True)
    conversion_factor = Column(Numeric(20, 10), nullable=True)
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    unit = relationship("Unit", back_populates="versions")
