from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company, get_current_user
from app.schemas.common import ApiResponse
from app.schemas.quotation import (
    QuotationCreate, QuotationResponse, QuotationListResponse, QuotationAcceptRequest
)
from app.services.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["Quotations"])

@router.post("/", response_model=ApiResponse[QuotationResponse])
def create_quotation(request: QuotationCreate, company = Depends(get_current_company), user = Depends(get_current_user), db: Session = Depends(get_db)):
    q = QuotationService.create_quotation(db, str(company.id), request.model_dump(), str(user.id))
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.get("/", response_model=ApiResponse[QuotationListResponse])
def list_quotations(quotation_type: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    quotations = QuotationService.list_quotations(db, str(company.id), quotation_type)
    return ApiResponse(success=True, data=QuotationListResponse(
        items=[_quotation_to_response(q) for q in quotations],
        total=len(quotations)
    ))

@router.get("/{quotation_id}", response_model=ApiResponse[QuotationResponse])
def get_quotation(quotation_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.get_quotation(db, str(company.id), quotation_id)
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.post("/{quotation_id}/approve", response_model=ApiResponse[QuotationResponse])
def approve_quotation(quotation_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.approve_quotation(db, str(company.id), quotation_id)
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.post("/{quotation_id}/accept", response_model=ApiResponse[QuotationResponse])
def accept_quotation(quotation_id: str, request: QuotationAcceptRequest, company = Depends(get_current_company), user = Depends(get_current_user), db: Session = Depends(get_db)):
    q = QuotationService.accept_quotation(db, str(company.id), quotation_id, str(user.id), request.acceptance_method)
    return ApiResponse(success=True, data=_quotation_to_response(q))

def _quotation_to_response(q) -> QuotationResponse:
    lines = []
    for l in q.lines:
        lines.append({
            "id": l.id,
            "item_id": l.item_id,
            "item_name_snapshot": l.item_name_snapshot,
            "description": l.description,
            "hsn_sac_snapshot": l.hsn_sac_snapshot,
            "sku_snapshot": l.sku_snapshot,
            "quantity": float(l.quantity),
            "converted_quantity": float(l.converted_quantity),
            "unit_id": l.unit_id,
            "unit_snapshot": l.unit_snapshot,
            "rate": float(l.rate),
            "discount_type": l.discount_type,
            "discount_value": float(l.discount_value),
            "discount_amount": float(l.discount_amount),
            "tax_treatment": l.tax_treatment,
            "gst_rate": float(l.gst_rate),
            "taxable_value": float(l.taxable_value),
            "cgst_amount": float(l.cgst_amount),
            "sgst_amount": float(l.sgst_amount),
            "igst_amount": float(l.igst_amount),
            "cess_amount": float(l.cess_amount),
            "line_total": float(l.line_total)
        })
        
    return QuotationResponse(
        id=q.id,
        quotation_number=q.quotation_number,
        quotation_type=q.quotation_type.value,
        tax_treatment=q.tax_treatment,
        party_id=q.party_id,
        quotation_date=q.quotation_date,
        valid_until=q.valid_until,
        status=q.status.value,
        revision=q.revision,
        place_of_supply=q.place_of_supply,
        subtotal=float(q.subtotal),
        discount_total=float(q.discount_total),
        taxable_total=float(q.taxable_total),
        cgst_total=float(q.cgst_total),
        sgst_total=float(q.sgst_total),
        igst_total=float(q.igst_total),
        cess_total=float(q.cess_total),
        round_off=float(q.round_off),
        grand_total=float(q.grand_total),
        notes=q.notes,
        terms=q.terms,
        accepted_at=q.accepted_at,
        accepted_by=q.accepted_by,
        acceptance_method=q.acceptance_method,
        fully_converted=q.fully_converted,
        created_at=q.created_at,
        lines=lines
    )
