from sqlalchemy.orm import Session
from app.models.estimate import Estimate, EstimateLine, EstimateStatus
from app.models.boq import BOQItemType
from app.models import DocumentLink
from app.core.exceptions import NotFoundException, ValidationException
import uuid
from datetime import datetime, timezone
from decimal import Decimal

def utc_now():
    return datetime.now(timezone.utc)

class EstimateService:
    @staticmethod
    def create_estimate(db: Session, company_id: str, data: dict, user_id: str = None) -> Estimate:
        estimate = Estimate(
            id=str(uuid.uuid4()),
            company_id=company_id,
            estimate_number=f"EST-{str(uuid.uuid4())[:6].upper()}",
            boq_id=data.get("boq_id"),
            party_id=data.get("party_id"),
            estimate_date=data["estimate_date"],
            valid_until=data.get("valid_until"),
            status=EstimateStatus.DRAFT,
            created_by=user_id
        )
        
        db.add(estimate)
        
        material_cost = Decimal('0')
        labour_cost = Decimal('0')
        service_cost = Decimal('0')
        other_cost = Decimal('0')
        
        total_markup_amount = Decimal('0')
        total_selling_value = Decimal('0')
        
        for line_data in data["lines"]:
            qty = Decimal(str(line_data["quantity"]))
            cost_rate = Decimal(str(line_data.get("cost_rate") or '0'))
            markup_percent = Decimal(str(line_data.get("markup_percent") or '0'))
            
            cost_amount = qty * cost_rate
            markup_amount = cost_amount * (markup_percent / Decimal('100'))
            selling_amount = cost_amount + markup_amount
            selling_rate = selling_amount / qty if qty > 0 else Decimal('0')
            
            item_type_val = line_data.get("item_type", "MATERIAL")
            
            if item_type_val == "MATERIAL":
                material_cost += cost_amount
            elif item_type_val == "LABOUR":
                labour_cost += cost_amount
            elif item_type_val == "SERVICE":
                service_cost += cost_amount
            else:
                other_cost += cost_amount
                
            total_markup_amount += markup_amount
            total_selling_value += selling_amount
            
            line = EstimateLine(
                id=str(uuid.uuid4()),
                estimate_id=estimate.id,
                item_name_snapshot=line_data["item_name_snapshot"],
                item_type=item_type_val,
                quantity=qty,
                unit_snapshot=line_data.get("unit_snapshot"),
                cost_rate=cost_rate,
                cost_amount=cost_amount,
                markup_percent=markup_percent,
                markup_amount=markup_amount,
                selling_rate=selling_rate,
                selling_amount=selling_amount
            )
            db.add(line)
            
        total_cost = material_cost + labour_cost + service_cost + other_cost
        
        estimate.material_cost = material_cost
        estimate.labour_cost = labour_cost
        estimate.service_cost = service_cost
        estimate.other_cost = other_cost
        estimate.total_cost = total_cost
        estimate.markup_amount = total_markup_amount
        estimate.estimated_selling_value = total_selling_value
        estimate.grand_total = total_selling_value # Simplification, GST logic can be added later
        
        # Link BOQ if applicable
        if data.get("boq_id"):
            doc_link = DocumentLink(
                company_id=company_id,
                source_type="BOQ",
                source_id=data["boq_id"],
                target_type="ESTIMATE",
                target_id=estimate.id,
                relationship_type="ESTIMATED_FROM_BOQ",
                created_by=user_id
            )
            db.add(doc_link)
            
        db.commit()
        db.refresh(estimate)
        return estimate

    @staticmethod
    def get_estimate(db: Session, company_id: str, estimate_id: str) -> Estimate:
        estimate = db.query(Estimate).filter(Estimate.id == estimate_id, Estimate.company_id == company_id).first()
        if not estimate:
            raise NotFoundException("Estimate not found")
        return estimate

    @staticmethod
    def list_estimates(db: Session, company_id: str) -> list[Estimate]:
        return db.query(Estimate).filter(Estimate.company_id == company_id).order_by(Estimate.created_at.desc()).all()

    @staticmethod
    def approve_estimate(db: Session, company_id: str, estimate_id: str) -> Estimate:
        estimate = EstimateService.get_estimate(db, company_id, estimate_id)
        if estimate.status != EstimateStatus.DRAFT:
            raise ValidationException("Only DRAFT Estimate can be approved")
            
        estimate.status = EstimateStatus.APPROVED
        db.commit()
        db.refresh(estimate)
        return estimate
