from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.estimate import EstimateCreate, EstimateResponse, EstimateListResponse
from app.services.estimate_service import EstimateService

router = APIRouter(prefix="/estimates", tags=["Estimates"])

@router.post("/", response_model=ApiResponse[EstimateResponse])
def create_estimate(request: EstimateCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.create_estimate(db, str(company.id), request.model_dump(), None)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

@router.get("/", response_model=ApiResponse[EstimateListResponse])
def list_estimates(company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimates = EstimateService.list_estimates(db, str(company.id))
    return ApiResponse(success=True, data=EstimateListResponse(
        items=[_estimate_to_response(e) for e in estimates],
        total=len(estimates)
    ))

@router.get("/{estimate_id}", response_model=ApiResponse[EstimateResponse])
def get_estimate(estimate_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.get_estimate(db, str(company.id), estimate_id)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

@router.post("/{estimate_id}/approve", response_model=ApiResponse[EstimateResponse])
def approve_estimate(estimate_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.approve_estimate(db, str(company.id), estimate_id)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

def _estimate_to_response(estimate) -> EstimateResponse:
    lines = []
    for l in estimate.lines:
        lines.append({
            "id": l.id,
            "item_name_snapshot": l.item_name_snapshot,
            "item_type": l.item_type,
            "quantity": float(l.quantity),
            "unit_snapshot": l.unit_snapshot,
            "cost_rate": float(l.cost_rate),
            "cost_amount": float(l.cost_amount),
            "markup_percent": float(l.markup_percent),
            "markup_amount": float(l.markup_amount),
            "selling_rate": float(l.selling_rate),
            "selling_amount": float(l.selling_amount)
        })
        
    return EstimateResponse(
        id=estimate.id,
        estimate_number=estimate.estimate_number,
        boq_id=estimate.boq_id,
        party_id=estimate.party_id,
        estimate_date=estimate.estimate_date,
        valid_until=estimate.valid_until,
        version=estimate.version,
        status=estimate.status.value,
        material_cost=float(estimate.material_cost),
        labour_cost=float(estimate.labour_cost),
        service_cost=float(estimate.service_cost),
        other_cost=float(estimate.other_cost),
        total_cost=float(estimate.total_cost),
        markup_amount=float(estimate.markup_amount),
        estimated_selling_value=float(estimate.estimated_selling_value),
        gst_total=float(estimate.gst_total),
        grand_total=float(estimate.grand_total),
        created_at=estimate.created_at,
        updated_at=estimate.updated_at,
        lines=lines
    )
