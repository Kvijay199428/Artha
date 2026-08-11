import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_code = Column(String(20), unique=True, nullable=True)
    company_name = Column(String(200), nullable=False)
    legal_name = Column(String(200), nullable=True)
    trade_name = Column(String(200), nullable=True)
    ownership_type = Column(String(50), nullable=False)
    status = Column(String(20), default="SETUP_IN_PROGRESS")  # SETUP_IN_PROGRESS, ACTIVE, LOCKED, SUSPENDED, DEACTIVATED
    
    mobile = Column(String(20), nullable=False)
    office_phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False)
    website = Column(String(200), nullable=True)
    
    authorized_person_name = Column(String(100), nullable=False)
    authorized_person_designation = Column(String(100), nullable=True)
    authorized_person_mobile = Column(String(20), nullable=True)
    authorized_person_email = Column(String(100), nullable=True)
    
    logo_asset_id = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    version = Column(Integer, default=1)
    
    gst_details = relationship("CompanyGSTDetail", back_populates="company", uselist=False)
    addresses = relationship("CompanyAddress", back_populates="company")
    contacts = relationship("CompanyContact", back_populates="company")
    bank_accounts = relationship("CompanyBankAccount", back_populates="company")
    auth = relationship("CompanyAuth", back_populates="company", uselist=False)
    sessions = relationship("CompanySession", back_populates="company")
    audit_logs = relationship("AuditLog", back_populates="company")

class CompanyGSTDetail(Base):
    __tablename__ = "company_gst_details"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    gstin = Column(String(15), nullable=True)
    state_code = Column(String(2), nullable=True)
    state_name = Column(String(100), nullable=True)
    pan = Column(String(10), nullable=True)
    registration_number = Column(String(1), nullable=True)
    gstin_character_14 = Column(String(1), nullable=True)
    checksum = Column(String(1), nullable=True)
    gstin_validation_status = Column(String(20), default="NOT_VALIDATED")  # VALID, INVALID, NOT_VALIDATED
    external_verification_status = Column(String(20), default="NOT_VERIFIED")
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    company = relationship("Company", back_populates="gst_details")

class CompanyAddress(Base):
    __tablename__ = "company_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    address_type = Column(String(20), default="REGISTERED")  # REGISTERED, BILLING, SHIPPING, OFFICE
    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200), nullable=True)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False)
    state_code = Column(String(2), nullable=False)
    pincode = Column(String(10), nullable=False)
    country = Column(String(50), default="India")
    is_default = Column(Boolean, default=True)
    
    company = relationship("Company", back_populates="addresses")

class CompanyContact(Base):
    __tablename__ = "company_contacts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    contact_type = Column(String(20), default="PRIMARY")
    person_name = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    mobile = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    company = relationship("Company", back_populates="contacts")

class CompanyBankAccount(Base):
    __tablename__ = "company_bank_accounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    account_holder_name = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    ifsc = Column(String(20), nullable=False)
    bank_name = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=False)
    branch_address = Column(String(200), nullable=True)
    account_type = Column(String(20), default="Current")
    upi_id = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=True)
    status = Column(String(20), default="ACTIVE")
    
    company = relationship("Company", back_populates="bank_accounts")

class CompanyAsset(Base):
    __tablename__ = "company_assets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    asset_type = Column(String(30), nullable=False)  # COMPANY_LOGO, etc.
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=utc_now)

class CompanyAuth(Base):
    __tablename__ = "company_auth"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, unique=True)
    pin_hash = Column(String(255), nullable=False)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    company = relationship("Company", back_populates="auth")

class CompanySession(Base):
    __tablename__ = "company_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    session_token_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=False)
    last_activity_at = Column(DateTime, default=utc_now)
    revoked_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    company = relationship("Company", back_populates="sessions")