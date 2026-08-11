from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.party import PartyCreate, PartyUpdate, PartyResponse, PartyListResponse
from app.services.party_service import PartyService

router = APIRouter(prefix="/parties", tags=["Parties"])

@router.post("/", response_model=ApiResponse[PartyResponse])
def create_party(request: PartyCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.create_party(db, str(company.id), request.model_dump())
    return ApiResponse(success=True, data=_party_to_response(party))

@router.get("/", response_model=ApiResponse[PartyListResponse])
def list_parties(
    account_type: str = Query(None),
    search: str = Query(None),
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    parties = PartyService.list_parties(db, str(company.id), account_type, search)
    return ApiResponse(success=True, data=PartyListResponse(items=[_party_to_response(p) for p in parties]))

@router.get("/{party_id}", response_model=ApiResponse[PartyResponse])
def get_party(party_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.get_party(db, str(company.id), party_id)
    return ApiResponse(success=True, data=_party_to_response(party))

@router.put("/{party_id}", response_model=ApiResponse[PartyResponse])
def update_party(party_id: str, request: PartyUpdate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.update_party(db, str(company.id), party_id, request.model_dump(exclude_unset=True))
    return ApiResponse(success=True, data=_party_to_response(party))

def _party_to_response(party) -> PartyResponse:
    return PartyResponse(
        id=party.id,
        company_id=party.company_id,
        party_code=party.party_code,
        legal_name=party.legal_name,
        trade_name=party.trade_name,
        party_type=party.party_type,
        account_type=party.account_type,
        contact_person=party.contact_person,
        mobile=party.mobile,
        email=party.email,
        gstin=party.gstin,
        gst_registration_type=party.gst_registration_type,
        pan=party.pan,
        state=party.state,
        state_code=party.state_code,
        place_of_supply=party.place_of_supply,
        credit_limit=float(party.credit_limit) if party.credit_limit else None,
        credit_days=party.credit_days,
        payment_terms=party.payment_terms,
        notes=party.notes,
        status=party.status,
        created_at=party.created_at,
        updated_at=party.updated_at,
        addresses=[{
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
        } for a in party.addresses],
        bank_accounts=[{
            "id": b.id,
            "account_holder_name": b.account_holder_name,
            "bank_name": b.bank_name,
            "branch_name": b.branch_name,
            "account_number": b.account_number,
            "ifsc": b.ifsc,
            "upi_id": b.upi_id,
            "is_primary": b.is_primary,
        } for b in party.bank_accounts],
    )
