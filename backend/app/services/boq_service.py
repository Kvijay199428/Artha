from sqlalchemy.orm import Session
from app.models.boq import BOQ, BOQLine, BOQStatus, BOQItemType
from app.core.exceptions import NotFoundException, ValidationException
import uuid
from datetime import datetime, timezone
from decimal import Decimal

def utc_now():
    return datetime.now(timezone.utc)

class BOQService:
    @staticmethod
    def create_boq(db: Session, company_id: str, data: dict, user_id: str = None) -> BOQ:
        boq = BOQ(
            id=str(uuid.uuid4()),
            company_id=company_id,
            boq_number=f"BOQ-{str(uuid.uuid4())[:6].upper()}",
            project_name=data.get("project_name"),
            party_id=data.get("party_id"),
            boq_date=data["boq_date"],
            notes=data.get("notes"),
            status=BOQStatus.DRAFT,
            created_by=user_id
        )
        
        db.add(boq)
        
        for line_data in data["lines"]:
            qty = Decimal(str(line_data["quantity"]))
            rate = Decimal(str(line_data.get("estimated_rate") or '0'))
            amount = qty * rate
            
            line = BOQLine(
                id=str(uuid.uuid4()),
                boq_id=boq.id,
                parent_line_id=line_data.get("parent_line_id"),
                section=line_data.get("section"),
                item_type=BOQItemType(line_data.get("item_type", "MATERIAL")),
                item_id=line_data.get("item_id"),
                description=line_data["description"],
                specification=line_data.get("specification"),
                quantity=qty,
                unit_id=line_data.get("unit_id"),
                unit_snapshot=line_data.get("unit_snapshot"),
                quantity_formula=line_data.get("quantity_formula"),
                estimated_rate=rate,
                estimated_amount=amount,
                remarks=line_data.get("remarks"),
                sort_order=line_data.get("sort_order", 0)
            )
            db.add(line)
            
        db.commit()
        db.refresh(boq)
        return boq

    @staticmethod
    def get_boq(db: Session, company_id: str, boq_id: str) -> BOQ:
        boq = db.query(BOQ).filter(BOQ.id == boq_id, BOQ.company_id == company_id).first()
        if not boq:
            raise NotFoundException("BOQ not found")
        return boq

    @staticmethod
    def list_boqs(db: Session, company_id: str) -> list[BOQ]:
        return db.query(BOQ).filter(BOQ.company_id == company_id).order_by(BOQ.created_at.desc()).all()

    @staticmethod
    def approve_boq(db: Session, company_id: str, boq_id: str) -> BOQ:
        boq = BOQService.get_boq(db, company_id, boq_id)
        if boq.status != BOQStatus.DRAFT:
            raise ValidationException("Only DRAFT BOQ can be approved")
            
        boq.status = BOQStatus.APPROVED
        db.commit()
        db.refresh(boq)
        return boq
