from pydantic import BaseModel, Field
from typing import Optional

class CompanySetupRequest(BaseModel):
    # Business
    company_name: str = Field(..., min_length=2, max_length=200)
    ownership_type: str = Field(...)
    authorized_person_name: str = Field(..., min_length=1, max_length=100)
    authorized_person_designation: Optional[str] = Field(None, max_length=100)

    # GST / Tax
    gst_registered: bool = True
    gstin: Optional[str] = Field(None, max_length=15)
    tan: Optional[str] = Field(None, max_length=10)

    # Address
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")

    # Contact
    mobile: str = Field(..., min_length=7, max_length=20)
    mobile_country_code: str = Field(default="+91")
    mobile_e164: Optional[str] = Field(None, max_length=25)
    office_phone: Optional[str] = Field(None, max_length=20)
    office_phone_country_code: Optional[str] = Field(None, max_length=5)
    office_phone_e164: Optional[str] = Field(None, max_length=25)
    email: str = Field(..., max_length=100)
    website: Optional[str] = Field(None, max_length=300)

    # Bank — ALL OPTIONAL
    bank_account_holder_name: Optional[str] = Field(None, max_length=100)
    bank_account_number: Optional[str] = Field(None, max_length=50)
    bank_ifsc: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=100)
    bank_branch: Optional[str] = Field(None, max_length=100)
    bank_account_type: Optional[str] = Field(None, max_length=30)

    # Security
    pin: str = Field(..., min_length=4, max_length=4)
    confirm_pin: str = Field(..., min_length=4, max_length=4)

class LoginRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=4)

class LoginResponse(BaseModel):
    token: str
    company_name: str
    company_id: str

class CompanyProfileResponse(BaseModel):
    id: str
    company_name: str
    legal_name: Optional[str]
    ownership_type: str
    status: str
    mobile: str
    email: str
    authorized_person_name: str
    logo_url: Optional[str]
