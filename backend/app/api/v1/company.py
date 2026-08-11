from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.company import CompanyDetailResponse

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("/", response_model=ApiResponse[CompanyDetailResponse])
def get_company(company = Depends(get_current_company), db: Session = Depends(get_db)):
    from app.models.company import CompanyGSTDetail
    gst = db.query(CompanyGSTDetail).filter(CompanyGSTDetail.company_id == company.id).first()
    
    addresses = [{
        "id": a.id,
        "address_type": a.address_type,
        "address_line_1": a.address_line_1,
        "address_line_2": a.address_line_2,
        "city": a.city,
        "district": a.district,
        "state": a.state,
        "state_code": a.state_code,
        "pincode": a.pincode,
        "country": a.country,
        "is_default": a.is_default,
    } for a in company.addresses]
    
    banks = [{
        "id": b.id,
        "account_holder_name": b.account_holder_name,
        "account_number": b.account_number,
        "ifsc": b.ifsc,
        "bank_name": b.bank_name,
        "branch": b.branch,
        "account_type": b.account_type,
        "is_primary": b.is_primary,
    } for b in company.bank_accounts]
    
    return ApiResponse(success=True, data=CompanyDetailResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        trade_name=company.trade_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile=company.mobile,
        office_phone=company.office_phone,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        authorized_person_designation=company.authorized_person_designation,
        gst_details={
            "id": gst.id,
            "gstin": gst.gstin,
            "state_code": gst.state_code,
            "state_name": gst.state_name,
            "pan": gst.pan,
            "gstin_validation_status": gst.gstin_validation_status,
        } if gst else None,
        addresses=addresses,
        bank_accounts=banks,
        created_at=company.created_at,
        updated_at=company.updated_at,
    ))
