from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company, get_current_user
from app.schemas.common import ApiResponse
from app.schemas.boq import BOQCreate, BOQResponse, BOQListResponse
from app.services.boq_service import BOQService

router = APIRouter(prefix="/boqs", tags=["BOQ"])

@router.post("/", response_model=ApiResponse[BOQResponse])
def create_boq(request: BOQCreate, company = Depends(get_current_company), user = Depends(get_current_user), db: Session = Depends(get_db)):
    boq = BOQService.create_boq(db, str(company.id), request.model_dump(), str(user.id))
    return ApiResponse(success=True, data=_boq_to_response(boq))

@router.get("/", response_model=ApiResponse[BOQListResponse])
def list_boqs(company = Depends(get_current_company), db: Session = Depends(get_db)):
    boqs = BOQService.list_boqs(db, str(company.id))
    return ApiResponse(success=True, data=BOQListResponse(
        items=[_boq_to_response(b) for b in boqs],
        total=len(boqs)
    ))

@router.get("/{boq_id}", response_model=ApiResponse[BOQResponse])
def get_boq(boq_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    boq = BOQService.get_boq(db, str(company.id), boq_id)
    return ApiResponse(success=True, data=_boq_to_response(boq))

@router.post("/{boq_id}/approve", response_model=ApiResponse[BOQResponse])
def approve_boq(boq_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    boq = BOQService.approve_boq(db, str(company.id), boq_id)
    return ApiResponse(success=True, data=_boq_to_response(boq))

def _boq_to_response(boq) -> BOQResponse:
    lines = []
    for l in boq.lines:
        lines.append({
            "id": l.id,
            "parent_line_id": l.parent_line_id,
            "section": l.section,
            "item_type": l.item_type.value,
            "item_id": l.item_id,
            "description": l.description,
            "specification": l.specification,
            "quantity": float(l.quantity),
            "unit_id": l.unit_id,
            "unit_snapshot": l.unit_snapshot,
            "quantity_formula": l.quantity_formula,
            "estimated_rate": float(l.estimated_rate),
            "estimated_amount": float(l.estimated_amount),
            "remarks": l.remarks,
            "sort_order": l.sort_order
        })
        
    return BOQResponse(
        id=boq.id,
        boq_number=boq.boq_number,
        project_name=boq.project_name,
        party_id=boq.party_id,
        boq_date=boq.boq_date,
        version=boq.version,
        status=boq.status.value,
        notes=boq.notes,
        created_at=boq.created_at,
        updated_at=boq.updated_at,
        lines=lines
    )
