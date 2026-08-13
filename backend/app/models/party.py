import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Party(Base):
    __tablename__ = "parties"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_code = Column(String(50), nullable=True)
    legal_name = Column(String(200), nullable=False)
    trade_name = Column(String(200), nullable=True)
    party_type = Column(String(50), nullable=False)  # Individual, Proprietorship, Partnership, LLP, Company, Other
    account_type = Column(String(20), nullable=False)  # CUSTOMER, SUPPLIER, BOTH
    contact_person = Column(String(100), nullable=True)
    mobile_country_code = Column(String(5), default="+91", nullable=True)
    mobile = Column(String(20), nullable=True)
    mobile_e164 = Column(String(20), nullable=True)
    alternate_mobile = Column(String(20), nullable=True)
    office_phone_country_code = Column(String(5), nullable=True)
    office_phone = Column(String(20), nullable=True)
    office_phone_e164 = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(300), nullable=True)
    gstin = Column(String(15), nullable=True)
    gst_registration_type = Column(String(30), default="Regular")  # Regular, Composition, Unregistered, SEZ
    gstin_status = Column(String(20), default="Unknown")  # Active, Cancelled, Suspended
    pan = Column(String(10), nullable=True)
    tan = Column(String(10), nullable=True)
    state = Column(String(100), nullable=True)
    state_code = Column(String(2), nullable=True)
    place_of_supply = Column(String(100), nullable=True)
    credit_limit = Column(Numeric(15, 2), nullable=True)
    credit_days = Column(Integer, nullable=True)
    payment_terms = Column(String(50), nullable=True)
    default_price_list = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    addresses = relationship("PartyAddress", back_populates="party", cascade="all, delete-orphan")
    bank_accounts = relationship("PartyBankAccount", back_populates="party", cascade="all, delete-orphan")
    ledger_entries = relationship("PartyLedgerEntry", back_populates="party")

class PartyAddress(Base):
    __tablename__ = "party_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    address_type = Column(String(20), default="BILLING")  # REGISTERED, BILLING, SHIPPING, OFFICE, WAREHOUSE, OTHER
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
    
    party = relationship("Party", back_populates="addresses")

class PartyBankAccount(Base):
    __tablename__ = "party_bank_accounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    account_holder_name = Column(String(100), nullable=True)
    bank_name = Column(String(100), nullable=True)
    branch_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc = Column(String(20), nullable=True)
    account_type = Column(String(30), default="CURRENT", nullable=True)  # SAVINGS, CURRENT, CASH_CREDIT, OVERDRAFT, NRE, NRO, OTHER
    upi_id = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=True)
    status = Column(String(20), default="ACTIVE")
    
    party = relationship("Party", back_populates="bank_accounts")

class PartyLedgerEntry(Base):
    __tablename__ = "party_ledger_entries"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    posting_date = Column(DateTime, default=utc_now)
    transaction_type = Column(String(50), nullable=False)  # Invoice, Receipt, Payment, Credit Note, Debit Note, Journal, Opening
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(String(36), nullable=True)
    reference_number = Column(String(50), nullable=True)
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    currency = Column(String(3), default="INR")
    narration = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    party = relationship("Party", back_populates="ledger_entries")

class PaymentAllocation(Base):
    __tablename__ = "payment_allocations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    payment_id = Column(String(36), nullable=False)  # Can reference PartyLedgerEntry or Payment table
    invoice_id = Column(String(36), nullable=False)
    allocated_amount = Column(Numeric(15, 2), nullable=False)
    allocation_date = Column(DateTime, default=utc_now)
