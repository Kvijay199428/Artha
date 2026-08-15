from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.adjustment import AdjustmentNoteCreate, AdjustmentNoteResponse, NoteAllocationCreate, NoteAllocationResponse
from app.services.adjustment import FinancialAdjustmentService
from app.models.adjustment import AdjustmentNote
from app.dependencies.auth import get_current_company

router = APIRouter(prefix="/adjustment-notes", tags=["Adjustments"])

@router.post("/credit-notes", response_model=AdjustmentNoteResponse)
def create_credit_note(
    *,
    db: Session = Depends(get_db),
    note_in: AdjustmentNoteCreate,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    return service.create_credit_note(note_in=note_in, company_id=current_company.id)

@router.post("/debit-notes", response_model=AdjustmentNoteResponse)
def create_debit_note(
    *,
    db: Session = Depends(get_db),
    note_in: AdjustmentNoteCreate,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    return service.create_debit_note(note_in=note_in, company_id=current_company.id)

@router.post("/{note_id}/post", response_model=AdjustmentNoteResponse)
def post_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.post_note(note_id=note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note
