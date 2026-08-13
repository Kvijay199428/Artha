from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PartyAddressCreate(BaseModel):
    address_type: str = Field(default="BILLING")
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: Optional[str] = Field(None, max_length=200)
    landmark: Optional[str] = Field(None, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")
    is_default: bool = True

class PartyBankAccountCreate(BaseModel):
    account_holder_name: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=100)
    branch_name: Optional[str] = Field(None, max_length=100)
    account_number: Optional[str] = Field(None, max_length=50)
    ifsc: Optional[str] = Field(None, max_length=20)
    account_type: Optional[str] = Field("CURRENT", max_length=30)
    upi_id: Optional[str] = Field(None, max_length=100)
    is_primary: bool = True

class PartyCreate(BaseModel):
    legal_name: str = Field(..., min_length=1, max_length=200)
    trade_name: Optional[str] = Field(None, max_length=200)
    party_type: str = Field(default="Proprietorship")
    account_type: str = Field(..., pattern="^(CUSTOMER|SUPPLIER|BOTH)$")
    contact_person: Optional[str] = Field(None, max_length=100)
    mobile_country_code: Optional[str] = Field(default="+91", max_length=5)
    mobile: Optional[str] = Field(None, max_length=20)
    mobile_e164: Optional[str] = Field(None, max_length=20)
    alternate_mobile: Optional[str] = Field(None, max_length=20)
    office_phone_country_code: Optional[str] = Field(None, max_length=5)
    office_phone: Optional[str] = Field(None, max_length=20)
    office_phone_e164: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=300)
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: str = Field(default="Regular")
    pan: Optional[str] = Field(None, max_length=10)
    tan: Optional[str] = Field(None, max_length=10)
    state: Optional[str] = Field(None, max_length=100)
    state_code: Optional[str] = Field(None, max_length=2)
    place_of_supply: Optional[str] = Field(None, max_length=100)
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    payment_terms: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    addresses: list[PartyAddressCreate] = []
    bank_accounts: list[PartyBankAccountCreate] = []

class PartyUpdate(BaseModel):
    legal_name: Optional[str] = Field(None, min_length=1, max_length=200)
    trade_name: Optional[str] = Field(None, max_length=200)
    party_type: Optional[str] = None
    account_type: Optional[str] = Field(None, pattern="^(CUSTOMER|SUPPLIER|BOTH)$")
    contact_person: Optional[str] = None
    mobile_country_code: Optional[str] = None
    mobile: Optional[str] = None
    mobile_e164: Optional[str] = None
    alternate_mobile: Optional[str] = None
    office_phone_country_code: Optional[str] = None
    office_phone: Optional[str] = None
    office_phone_e164: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: Optional[str] = None
    pan: Optional[str] = Field(None, max_length=10)
    tan: Optional[str] = Field(None, max_length=10)
    state: Optional[str] = None
    state_code: Optional[str] = None
    place_of_supply: Optional[str] = None
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")

class PartyResponse(BaseModel):
    id: str
    company_id: str
    party_code: Optional[str]
    legal_name: str
    trade_name: Optional[str]
    party_type: str
    account_type: str
    contact_person: Optional[str]
    mobile_country_code: Optional[str]
    mobile: Optional[str]
    mobile_e164: Optional[str]
    alternate_mobile: Optional[str]
    office_phone_country_code: Optional[str]
    office_phone: Optional[str]
    office_phone_e164: Optional[str]
    email: Optional[str]
    website: Optional[str]
    gstin: Optional[str]
    gst_registration_type: str
    pan: Optional[str]
    tan: Optional[str]
    state: Optional[str]
    state_code: Optional[str]
    place_of_supply: Optional[str]
    credit_limit: Optional[float]
    credit_days: Optional[int]
    payment_terms: Optional[str]
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    addresses: list[dict] = []
    bank_accounts: list[dict] = []

class PartyListResponse(BaseModel):
    items: list[PartyResponse]
