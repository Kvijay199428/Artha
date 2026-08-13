from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.quotation import Quotation, QuotationLine, QuotationStatus, QuotationType
from app.models.master import Item
from app.models.party import Party
from app.core.exceptions import NotFoundException, ValidationException
import uuid
from datetime import datetime, timezone
from decimal import Decimal

def utc_now():
    return datetime.now(timezone.utc)

class QuotationService:
    @staticmethod
    def create_quotation(db: Session, company_id: str, data: dict, user_id: str = None) -> Quotation:
        party = db.query(Party).filter(Party.id == data["party_id"], Party.company_id == company_id).first()
        if not party:
            raise NotFoundException("Party not found")
            
        quotation = Quotation(
            id=str(uuid.uuid4()),
            company_id=company_id,
            quotation_number=f"QT-DRAFT-{str(uuid.uuid4())[:8].upper()}",
            quotation_type=QuotationType(data["quotation_type"]),
            tax_treatment=data["tax_treatment"],
            party_id=party.id,
            valid_until=data["valid_until"],
            place_of_supply=data["place_of_supply"],
            notes=data.get("notes"),
            terms=data.get("terms"),
            status=QuotationStatus.DRAFT,
            created_by=user_id
        )
        
        db.add(quotation)
        db.flush()
        
        subtotal = Decimal('0')
        discount_total = Decimal('0')
        taxable_total = Decimal('0')
        cgst_total = Decimal('0')
        sgst_total = Decimal('0')
        igst_total = Decimal('0')
        
        is_inter_state = False # In a real implementation, determine this based on Place of Supply vs Company State
        if data["tax_treatment"] == "GST":
            # Just a stub logic, usually you check states
            is_inter_state = False 
            
        for line_data in data["lines"]:
            qty = Decimal(str(line_data["quantity"]))
            rate = Decimal(str(line_data["rate"]))
            discount_val = Decimal(str(line_data.get("discount_value", 0)))
            discount_type = line_data.get("discount_type")
            
            line_subtotal = qty * rate
            line_discount_amount = Decimal('0')
            
            if discount_type == "PERCENTAGE":
                line_discount_amount = line_subtotal * (discount_val / Decimal('100'))
            elif discount_type == "FIXED":
                line_discount_amount = discount_val
                
            line_taxable = line_subtotal - line_discount_amount
            
            line_cgst = Decimal('0')
            line_sgst = Decimal('0')
            line_igst = Decimal('0')
            
            gst_rate = Decimal(str(line_data.get("gst_rate", 0)))
            
            if data["tax_treatment"] == "GST" and gst_rate > 0:
                if is_inter_state:
                    line_igst = line_taxable * (gst_rate / Decimal('100'))
                else:
                    line_cgst = line_taxable * (gst_rate / Decimal('200'))
                    line_sgst = line_taxable * (gst_rate / Decimal('200'))
                    
            line_total = line_taxable + line_cgst + line_sgst + line_igst
            
            q_line = QuotationLine(
                id=str(uuid.uuid4()),
                quotation_id=quotation.id,
                item_id=line_data.get("item_id"),
                item_name_snapshot=line_data["item_name_snapshot"],
                description=line_data.get("description"),
                sku_snapshot=line_data.get("sku_snapshot"),
                hsn_sac_snapshot=line_data.get("hsn_sac_snapshot"),
                quantity=qty,
                unit_id=line_data.get("unit_id"),
                unit_snapshot=line_data.get("unit_snapshot"),
                rate=rate,
                discount_type=discount_type,
                discount_value=discount_val,
                discount_amount=line_discount_amount,
                tax_treatment=data["tax_treatment"],
                gst_rate=gst_rate,
                taxable_value=line_taxable,
                cgst_amount=line_cgst,
                sgst_amount=line_sgst,
                igst_amount=line_igst,
                cess_amount=0,
                line_total=line_total
            )
            
            db.add(q_line)
            
            subtotal += line_subtotal
            discount_total += line_discount_amount
            taxable_total += line_taxable
            cgst_total += line_cgst
            sgst_total += line_sgst
            igst_total += line_igst
            
        quotation.subtotal = subtotal
        quotation.discount_total = discount_total
        quotation.taxable_total = taxable_total
        quotation.cgst_total = cgst_total
        quotation.sgst_total = sgst_total
        quotation.igst_total = igst_total
        quotation.grand_total = taxable_total + cgst_total + sgst_total + igst_total
        
        db.commit()
        db.refresh(quotation)
        return quotation

    @staticmethod
    def list_quotations(db: Session, company_id: str, q_type: str = None) -> list[Quotation]:
        query = db.query(Quotation).filter(Quotation.company_id == company_id)
        if q_type:
            query = query.filter(Quotation.quotation_type == q_type)
        return query.order_by(Quotation.created_at.desc()).all()

    @staticmethod
    def get_quotation(db: Session, company_id: str, quotation_id: str) -> Quotation:
        q = db.query(Quotation).filter(Quotation.id == quotation_id, Quotation.company_id == company_id).first()
        if not q:
            raise NotFoundException("Quotation not found")
        return q
        
    @staticmethod
    def approve_quotation(db: Session, company_id: str, quotation_id: str) -> Quotation:
        q = QuotationService.get_quotation(db, company_id, quotation_id)
        if q.status != QuotationStatus.DRAFT:
            raise ValidationException("Only DRAFT quotations can be approved")
            
        q.status = QuotationStatus.APPROVED
        q.quotation_number = f"QT-{str(uuid.uuid4())[:6].upper()}"
        
        db.commit()
        db.refresh(q)
        return q
        
    @staticmethod
    def accept_quotation(db: Session, company_id: str, quotation_id: str, user_id: str, acceptance_method: str = "USER_ACCEPTED") -> Quotation:
        q = QuotationService.get_quotation(db, company_id, quotation_id)
        
        # Validations
        if q.status not in [QuotationStatus.APPROVED, QuotationStatus.SENT, QuotationStatus.VIEWED]:
            raise ValidationException("Quotation is not in a valid state to be accepted")
            
        if q.valid_until and q.valid_until < utc_now():
            q.status = QuotationStatus.EXPIRED
            db.commit()
            raise ValidationException("Quotation has expired")
            
        q.status = QuotationStatus.ACCEPTED
        q.accepted_at = utc_now()
        q.accepted_by = user_id
        q.acceptance_method = acceptance_method
        
        db.commit()
        db.refresh(q)
        return q
