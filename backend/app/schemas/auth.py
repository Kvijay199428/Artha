from pydantic import BaseModel, Field

class CompanySetupRequest(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    ownership_type: str = Field(...)
    gst_registered: bool = True
    gstin: str | None = Field(None, max_length=15)
    tan: str | None = Field(None, max_length=10)
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: str | None = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    district: str | None = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")
    mobile_country_code: str = Field(default="+91")
    mobile: str = Field(..., min_length=10, max_length=20)
    office_phone_country_code: str | None = Field(None, max_length=5)
    office_phone: str | None = Field(None, max_length=20)
    email: str = Field(..., max_length=100)
    authorized_person_name: str = Field(..., min_length=1, max_length=100)
    authorized_person_designation: str | None = Field(None, max_length=100)
    bank_account_holder_name: str = Field(..., min_length=1, max_length=100)
    bank_account_number: str = Field(..., min_length=4, max_length=50)
    bank_ifsc: str = Field(..., min_length=11, max_length=20)
    bank_name: str | None = Field(None, max_length=100)
    bank_branch: str = Field(..., min_length=1, max_length=100)
    bank_account_type: str = Field(default="Current")
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
    legal_name: str | None
    ownership_type: str
    status: str
    mobile: str
    email: str
    authorized_person_name: str
    logo_url: str | None
