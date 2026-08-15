from sqlalchemy.orm import Session
from app.models.adjustment import AdjustmentNote, AdjustmentNoteLine
from app.schemas.adjustment import AdjustmentNoteCreate
from app.models.audit import AuditLog
from typing import Optional, Tuple, List

class FinancialAdjustmentService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_notes(self, company_id: str, note_type: Optional[str] = None) -> Tuple[List[AdjustmentNote], int]:
        query = self.db.query(AdjustmentNote).filter(AdjustmentNote.company_id == company_id)
        if note_type:
            query = query.filter(AdjustmentNote.note_type == note_type)
        total = query.count()
        items = query.order_by(AdjustmentNote.created_at.desc()).all()
        return items, total

    def get_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        return self.db.query(AdjustmentNote).filter(
            AdjustmentNote.id == note_id,
            AdjustmentNote.company_id == company_id
        ).first()

    def create_credit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        return self._create_note(note_in, company_id, "CREDIT_NOTE")
        
    def create_debit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        return self._create_note(note_in, company_id, "DEBIT_NOTE")
        
    def _create_note(self, note_in: AdjustmentNoteCreate, company_id: str, note_type: str) -> AdjustmentNote:
        note_data = note_in.dict(exclude={"lines"})
        note = AdjustmentNote(
            **note_data,
            company_id=company_id,
            note_type=note_type,
            note_number=f"{'CN' if note_type == 'CREDIT_NOTE' else 'DN'}-TMP",
            status="DRAFT"
        )
        self.db.add(note)
        self.db.flush()
        
        for line_in in note_in.lines:
            line = AdjustmentNoteLine(**line_in.dict(), adjustment_note_id=note.id)
            self.db.add(line)
            
        self.db.commit()
        self.db.refresh(note)
        return note
        
    def post_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status in ["DRAFT", "APPROVED"]:
            note.status = "POSTED"
            # Implement Ledger Posting later
            self.db.commit()
            self.db.refresh(note)
        return note

    def approve_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status == "DRAFT":
            note.status = "APPROVED"
            self.db.commit()
            self.db.refresh(note)
        return note

    def cancel_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status in ["DRAFT", "APPROVED"]:
            note.status = "CANCELLED"
            self.db.commit()
            self.db.refresh(note)
        return note

    def reverse_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status == "POSTED":
            note.status = "REVERSED"
            # Implement Ledger Reversal later
            self.db.commit()
            self.db.refresh(note)
        return note
