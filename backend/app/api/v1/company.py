from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.company import CompanyDetailResponse, CompanyUpdate, CompanyLogoResponse
from app.services.company_service import CompanyService
from fastapi import UploadFile, File

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
        mobile_country_code=company.mobile_country_code,
        mobile=company.mobile,
        mobile_e164=company.mobile_e164,
        office_phone_country_code=company.office_phone_country_code,
        office_phone=company.office_phone,
        office_phone_e164=company.office_phone_e164,
        email=company.email,
        website=company.website,
        logo_url=company.logo_url,
        authorized_person_name=company.authorized_person_name,
        authorized_person_designation=company.authorized_person_designation,
        gst_details={
            "id": gst.id,
            "gstin": gst.gstin,
            "state_code": gst.state_code,
            "state_name": gst.state_name,
            "pan": gst.pan,
            "tan": gst.tan,
            "gstin_validation_status": gst.gstin_validation_status,
        } if gst else None,
        addresses=addresses,
        bank_accounts=banks,
        created_at=company.created_at,
        updated_at=company.updated_at,
    ))

@router.put("/", response_model=ApiResponse[CompanyDetailResponse])
def update_company(
    data: CompanyUpdate,
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    updated = CompanyService.update_company(db, company.id, data.model_dump(exclude_unset=True))
    return get_company(company=updated, db=db)

@router.post("/logo", response_model=ApiResponse[CompanyLogoResponse])
async def upload_company_logo(
    file: UploadFile = File(...),
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    from app.services.file_storage_service import FileStorageService
    logo_metadata = await FileStorageService.save_company_logo(company.id, file)
    company = CompanyService.update_company_logo(db, company.id, logo_metadata)
    return ApiResponse(success=True, data=CompanyLogoResponse(logo_url=company.logo_url, asset_id=company.logo_asset_id))

@router.delete("/logo", response_model=ApiResponse[bool])
def delete_company_logo(
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    CompanyService.update_company_logo(db, company.id, None)
    return ApiResponse(success=True, data=True)

@router.get("/logo/{company_id}")
def get_company_logo_public(company_id: str, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    from app.models.company import CompanyAsset
    asset = db.query(CompanyAsset).filter(CompanyAsset.company_id == company_id, CompanyAsset.asset_type == "COMPANY_LOGO").order_by(CompanyAsset.created_at.desc()).first()
    if not asset:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Logo not found")
    from app.services.file_storage_service import FileStorageService
    file_path = FileStorageService.get_file_path(asset.file_path)
    return FileResponse(file_path, media_type=asset.mime_type)

@router.get("/logo")
def get_company_logo(company = Depends(get_current_company), db: Session = Depends(get_db)):
    return get_company_logo_public(company.id, db)
