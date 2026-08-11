from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.exceptions import ValidationException
from app.schemas.auth import CompanySetupRequest, LoginRequest, LoginResponse, CompanyProfileResponse
from app.schemas.common import ApiResponse
from app.services.company_service import CompanyService
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_company

router = APIRouter(prefix="/auth", tags=["Authentication"])

class PinResetRequest(BaseModel):
    old_pin: str
    new_pin: str
    confirm_pin: str

@router.post("/setup", response_model=ApiResponse[CompanyProfileResponse])
def setup_company(request: CompanySetupRequest, db: Session = Depends(get_db)):
    company = CompanyService.create_company(db, request)
    return ApiResponse(success=True, data=CompanyProfileResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile=company.mobile,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        logo_url=None
    ))

@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # For simplicity, we assume single company mode for now
    from app.models.company import Company
    company = db.query(Company).first()
    if not company:
        raise ValidationException("No company found. Please complete setup first.")
    
    token = AuthService.authenticate(db, company.id, request.pin)
    return ApiResponse(success=True, data=LoginResponse(
        token=token,
        company_name=company.company_name,
        company_id=company.id
    ))

@router.get("/me", response_model=ApiResponse[CompanyProfileResponse])
def get_me(company = Depends(get_current_company)):
    return ApiResponse(success=True, data=CompanyProfileResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile=company.mobile,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        logo_url=None
    ))
