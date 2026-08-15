from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.adjustment import AdjustmentNoteCreate, AdjustmentNoteResponse, AdjustmentNoteListResponse, NoteAllocationCreate, NoteAllocationResponse
from app.schemas.common import ApiResponse
from app.services.adjustment import FinancialAdjustmentService
from app.dependencies.auth import get_current_company

router = APIRouter(prefix="/adjustment-notes", tags=["Adjustments"])

@router.get("", response_model=ApiResponse[AdjustmentNoteListResponse])
def get_adjustment_notes(
    *,
    db: Session = Depends(get_db),
    note_type: Optional[str] = None,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    items, total = service.get_notes(company_id=current_company.id, note_type=note_type)
    return ApiResponse(success=True, data=AdjustmentNoteListResponse(items=items, total=total))

@router.post("", response_model=ApiResponse[AdjustmentNoteResponse])
def create_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_in: AdjustmentNoteCreate,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    if note_in.note_type == "CREDIT_NOTE":
        note = service.create_credit_note(note_in=note_in, company_id=current_company.id)
    else:
        note = service.create_debit_note(note_in=note_in, company_id=current_company.id)
    return ApiResponse(success=True, data=note)

@router.get("/{note_id}", response_model=ApiResponse[AdjustmentNoteResponse])
def get_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.get_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/post", response_model=ApiResponse[AdjustmentNoteResponse])
def post_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.post_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/approve", response_model=ApiResponse[AdjustmentNoteResponse])
def approve_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.approve_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/cancel", response_model=ApiResponse[AdjustmentNoteResponse])
def cancel_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.cancel_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/reverse", response_model=ApiResponse[AdjustmentNoteResponse])
def reverse_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.reverse_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.get("/{note_id}/pdf")
def get_adjustment_note_pdf(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    raise HTTPException(status_code=501, detail="PDF generation not implemented yet")

