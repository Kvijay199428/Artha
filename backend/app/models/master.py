import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Numeric, Boolean
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class GSTStateCode(Base):
    __tablename__ = "gst_state_codes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(2), unique=True, nullable=False)
    state_name = Column(String(100), nullable=False)
    union_territory = Column(Boolean, default=False)

class GSTRate(Base):
    __tablename__ = "gst_rates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = Column(Numeric(5, 2), nullable=False)
    display_name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")

class HSNSACCode(Base):
    __tablename__ = "hsn_sac_codes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)  # HSN, SAC
    description = Column(String(500), nullable=True)
    gst_rate_id = Column(String(36), nullable=True)
    applicable_from = Column(DateTime, nullable=True)
    applicable_to = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")
