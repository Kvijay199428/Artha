from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.return_order import ReturnOrder, ReturnOrderLine, ReturnType, ReturnStatus, FinancialStatus, ReturnSettlement, SettlementType
from app.models.order import SupplyOrder, SupplyOrderLine, OrderStatus
from app.core.exceptions import NotFoundException, ValidationException
import uuid
from decimal import Decimal

class ReturnService:
    @staticmethod
    def get_returnable_lines(db: Session, company_id: str, order_id: str):
        order = db.query(SupplyOrder).filter(SupplyOrder.id == order_id, SupplyOrder.company_id == company_id).first()
        if not order:
            raise NotFoundException("Order not found")
            
        lines_data = []
        for line in order.lines:
            # Calculate previously returned quantity
            prev_returned = db.query(func.sum(ReturnOrderLine.return_quantity)).join(ReturnOrder).filter(
                ReturnOrderLine.original_order_line_id == line.id,
                ReturnOrder.status != ReturnStatus.CANCELLED
            ).scalar() or Decimal('0')
            
            returnable = line.quantity - prev_returned
            if returnable > 0:
                lines_data.append({
                    "original_order_line_id": line.id,
                    "item_name_snapshot": line.item_name_snapshot,
                    "unit_symbol_snapshot": line.unit_symbol_snapshot,
                    "rate": float(line.rate),
                    "gst_rate": float(line.gst_rate),
                    "original_quantity": float(line.quantity),
                    "previously_returned_quantity": float(prev_returned),
                    "returnable_quantity": float(returnable)
                })
                
        return {
            "order_id": order.id,
            "order_type": order.order_type.value,
            "tax_treatment": order.tax_treatment.value,
            "lines": lines_data
        }

    @staticmethod
    def create_return(db: Session, company_id: str, data: dict, user_id: str = None) -> ReturnOrder:
        order = db.query(SupplyOrder).filter(SupplyOrder.id == data["original_order_id"], SupplyOrder.company_id == company_id).first()
        if not order:
            raise NotFoundException("Order not found")
            
        ret_order = ReturnOrder(
            id=str(uuid.uuid4()),
            company_id=company_id,
            return_number=f"RET-DRAFT-{str(uuid.uuid4())[:8].upper()}",
            return_type=ReturnType(data["return_type"]),
            original_order_id=order.id,
            original_order_type=order.order_type.value,
            party_id=order.party_id,
            reason=data.get("reason"),
            created_by=user_id,
            status=ReturnStatus.DRAFT,
            financial_status=FinancialStatus.NOT_REQUIRED
        )
        
        db.add(ret_order)
        db.flush()
        
        subtotal = Decimal('0')
        taxable_total = Decimal('0')
        cgst_total = Decimal('0')
        sgst_total = Decimal('0')
        igst_total = Decimal('0')
        cess_total = Decimal('0')
        
        for line_data in data["lines"]:
            order_line = db.query(SupplyOrderLine).filter(SupplyOrderLine.id == line_data["original_order_line_id"]).first()
            if not order_line or order_line.supply_order_id != order.id:
                raise ValidationException(f"Invalid line {line_data['original_order_line_id']}")
                
            prev_returned = db.query(func.sum(ReturnOrderLine.return_quantity)).join(ReturnOrder).filter(
                ReturnOrderLine.original_order_line_id == order_line.id,
                ReturnOrder.status != ReturnStatus.CANCELLED
            ).scalar() or Decimal('0')
            
            return_qty = Decimal(str(line_data["return_quantity"]))
            
            if return_qty <= 0:
                raise ValidationException("Return quantity must be greater than 0")
            if prev_returned + return_qty > order_line.quantity:
                raise ValidationException(f"Cannot return {return_qty}. Only {order_line.quantity - prev_returned} remaining.")
                
            ratio = return_qty / order_line.quantity
            
            r_line = ReturnOrderLine(
                id=str(uuid.uuid4()),
                return_id=ret_order.id,
                original_order_line_id=order_line.id,
                item_id=order_line.item_id,
                item_name_snapshot=order_line.item_name_snapshot,
                sku_snapshot=order_line.sku_snapshot,
                hsn_sac_snapshot=order_line.hsn_sac_snapshot,
                unit_id=order_line.unit_id,
                unit_snapshot=order_line.unit_symbol_snapshot,
                
                original_quantity=order_line.quantity,
                previously_returned_quantity=prev_returned,
                return_quantity=return_qty,
                remaining_quantity=order_line.quantity - (prev_returned + return_qty),
                
                original_rate=order_line.rate,
                rate=order_line.rate,
                discount_type=order_line.discount_type,
                discount_value=order_line.discount_value,
                
                tax_treatment=order.tax_treatment.value,
                gst_rate=order_line.gst_rate,
                
                taxable_value=order_line.taxable_value * ratio,
                cgst_amount=order_line.cgst_amount * ratio,
                sgst_amount=order_line.sgst_amount * ratio,
                igst_amount=order_line.igst_amount * ratio,
                cess_amount=order_line.cess_amount * ratio,
                line_total=order_line.line_total * ratio,
                
                condition=line_data.get("condition", "GOOD"),
                warehouse_action=line_data.get("warehouse_action", "RETURN_TO_STOCK")
            )
            
            db.add(r_line)
            
            taxable_total += r_line.taxable_value
            cgst_total += r_line.cgst_amount
            sgst_total += r_line.sgst_amount
            igst_total += r_line.igst_amount
            cess_total += r_line.cess_amount
            
        ret_order.taxable_total = taxable_total
        ret_order.subtotal = taxable_total # Assuming no discount at doc level here
        ret_order.cgst_total = cgst_total
        ret_order.sgst_total = sgst_total
        ret_order.igst_total = igst_total
        ret_order.cess_total = cess_total
        ret_order.grand_total = taxable_total + cgst_total + sgst_total + igst_total + cess_total
        
        db.commit()
        db.refresh(ret_order)
        return ret_order

    @staticmethod
    def list_returns(db: Session, company_id: str, return_type: str = None) -> list[ReturnOrder]:
        query = db.query(ReturnOrder).filter(ReturnOrder.company_id == company_id)
        if return_type:
            query = query.filter(ReturnOrder.return_type == return_type)
        return query.order_by(ReturnOrder.created_at.desc()).all()

    @staticmethod
    def get_return(db: Session, company_id: str, return_id: str) -> ReturnOrder:
        ret = db.query(ReturnOrder).filter(ReturnOrder.id == return_id, ReturnOrder.company_id == company_id).first()
        if not ret:
            raise NotFoundException("Return not found")
        return ret
        
    @staticmethod
    def approve_return(db: Session, company_id: str, return_id: str, user_id: str) -> ReturnOrder:
        ret = ReturnService.get_return(db, company_id, return_id)
        if ret.status != ReturnStatus.DRAFT:
            raise ValidationException("Only DRAFT returns can be approved")
            
        ret.status = ReturnStatus.APPROVED
        ret.return_number = f"RET-{str(uuid.uuid4())[:6].upper()}"
        ret.approved_by = user_id
        
        db.commit()
        db.refresh(ret)
        return ret
        
    @staticmethod
    def post_return(db: Session, company_id: str, return_id: str) -> ReturnOrder:
        ret = ReturnService.get_return(db, company_id, return_id)
        if ret.status != ReturnStatus.APPROVED:
            raise ValidationException("Only APPROVED returns can be posted")
            
        ret.status = ReturnStatus.COMPLETED
        # Here we would integrate with accounting/inventory engines
        ret.financial_status = FinancialStatus.REFUND_PENDING
        
        db.commit()
        db.refresh(ret)
        return ret

    @staticmethod
    def add_settlement(db: Session, company_id: str, return_id: str, data: dict) -> ReturnSettlement:
        ret = ReturnService.get_return(db, company_id, return_id)
        if ret.status != ReturnStatus.COMPLETED:
            raise ValidationException("Can only settle COMPLETED returns")
            
        settled_so_far = sum(s.amount for s in ret.settlements)
        amount = Decimal(str(data["amount"]))
        
        if settled_so_far + amount > ret.grand_total:
            raise ValidationException("Settlement amount exceeds return total")
            
        settlement = ReturnSettlement(
            return_id=ret.id,
            settlement_type=SettlementType(data["settlement_type"]),
            amount=amount,
            reference_number=data.get("reference_number"),
            notes=data.get("notes")
        )
        db.add(settlement)
        
        new_total = settled_so_far + amount
        if new_total >= ret.grand_total:
            ret.financial_status = FinancialStatus.REFUNDED
        else:
            ret.financial_status = FinancialStatus.PARTIALLY_REFUNDED
            
        db.commit()
        db.refresh(settlement)
        return settlement
