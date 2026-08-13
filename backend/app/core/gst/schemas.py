from pydantic import BaseModel
from typing import Optional

class GSTINParseResult(BaseModel):
    gstin: str
    state_code: str
    state: Optional[str]
    is_union_territory: bool
    pan: str
    pan_holder_type: str
    entity_number: str
    default_character: str
    check_digit: str

class GSTINValidationResult(BaseModel):
    gstin: str
    valid: bool
    valid_length: bool
    valid_structure: bool
    valid_state_code: bool
    valid_checksum: bool
    errors: list[str]
    parsed: Optional[GSTINParseResult] = None
    level: str

class GSTStateResponse(BaseModel):
    code: str
    name: str
    is_union_territory: bool

class PhoneNumberInput(BaseModel):
    country_code: str
    number: str
    e164: Optional[str] = None

class BankAccountType(str):
    pass
