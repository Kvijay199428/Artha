from sqlalchemy.orm import Session
from app.models.adjustment import AdjustmentNote, AdjustmentNoteLine
from app.schemas.adjustment import AdjustmentNoteCreate
from app.models.audit import AuditLog

class FinancialAdjustmentService:
    def __init__(self, db: Session):
        self.db = db
        
    def create_credit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        # Business logic for credit note
        return self._create_note(note_in, company_id, "CREDIT_NOTE")
        
    def create_debit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        # Business logic for debit note
        return self._create_note(note_in, company_id, "DEBIT_NOTE")
        
    def _create_note(self, note_in: AdjustmentNoteCreate, company_id: str, note_type: str) -> AdjustmentNote:
        note_data = note_in.dict(exclude={"lines"})
        note = AdjustmentNote(
            **note_data,
            company_id=company_id,
            note_type=note_type,
            note_number=f"{'CN' if note_type == 'CREDIT_NOTE' else 'DN'}-TMP"
        )
        self.db.add(note)
        self.db.flush()
        
        for line_in in note_in.lines:
            line = AdjustmentNoteLine(**line_in.dict(), adjustment_note_id=note.id)
            self.db.add(line)
            
        self.db.commit()
        self.db.refresh(note)
        return note
        
    def post_note(self, note_id: str) -> AdjustmentNote:
        # Implement Ledger Posting
        note = self.db.query(AdjustmentNote).filter(AdjustmentNote.id == note_id).first()
        if note:
            note.status = "POSTED"
            self.db.commit()
            self.db.refresh(note)
        return note
