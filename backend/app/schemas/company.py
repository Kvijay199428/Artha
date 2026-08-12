from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CompanyAddressSchema(BaseModel):
    id: str
    address_type: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    district: Optional[str]
    state: str
    state_code: str
    pincode: str
    country: str
    is_default: bool

class CompanyBankAccountSchema(BaseModel):
    id: str
    account_holder_name: str
    account_number: str
    ifsc: str
    bank_name: Optional[str]
    branch: str
    account_type: str
    is_primary: bool

class CompanyGSTDetailSchema(BaseModel):
    id: str
    gstin: Optional[str]
    state_code: Optional[str]
    state_name: Optional[str]
    pan: Optional[str]
    gstin_validation_status: str

class CompanyDetailResponse(BaseModel):
    id: str
    company_name: str
    legal_name: Optional[str]
    trade_name: Optional[str]
    ownership_type: str
    status: str
    mobile: str
    office_phone: Optional[str]
    email: str
    authorized_person_name: str
    authorized_person_designation: Optional[str]
    gst_details: Optional[CompanyGSTDetailSchema]
    addresses: list[CompanyAddressSchema]
    bank_accounts: list[CompanyBankAccountSchema]
    created_at: datetime
    updated_at: datetime

class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    mobile: Optional[str] = None
    office_phone: Optional[str] = None
    email: Optional[str] = None
    authorized_person_name: Optional[str] = None
    authorized_person_designation: Optional[str] = None

class CompanyLogoResponse(BaseModel):
    logo_url: str
    asset_id: str
