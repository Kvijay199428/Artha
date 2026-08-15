from sqlalchemy.orm import Session
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import uuid

from app.models.order import SupplyOrder, SupplyOrderLine, OrderStatus, TaxTreatment, OrderType
from app.models.company import Company
from app.models.invoice import Invoice, InvoiceLine
from app.models.party import Party
from app.models.quotation import Quotation, QuotationStatus
from app.models import DocumentLink
from app.core.exceptions import NotFoundException, ValidationException
from app.utils.currency import amount_in_words

class OrderService:
    @staticmethod
    def calculate_order(db: Session, company_id: str, company: Company, data: dict) -> dict:
        tax_treatment = data["tax_treatment"]
        seller_state_code = company.state_code
        customer_state_code = data.get("place_of_supply") or seller_state_code
        
        is_interstate = (seller_state_code or "") != (customer_state_code or "")
        
        subtotal = Decimal("0")
        discount_total = Decimal("0")
        taxable_total = Decimal("0")
        cgst_total = Decimal("0")
        sgst_total = Decimal("0")
        igst_total = Decimal("0")
        
        calculated_lines = []
        
        for line_data in data["lines"]:
            rate = Decimal(str(line_data["rate"]))
            qty = Decimal(str(line_data["quantity"]))
            gross_amount = rate * qty
            
            discount_type = line_data.get("discount_type", "NONE")
            discount_value = Decimal(str(line_data.get("discount_value", 0)))
            
            line_discount = Decimal("0")
            if discount_type == "PERCENT":
                line_discount = gross_amount * (discount_value / Decimal("100"))
            elif discount_type == "FIXED":
                line_discount = discount_value
                
            taxable_value = gross_amount - line_discount
            if taxable_value < 0:
                taxable_value = Decimal("0")
                
            line_cgst = Decimal("0")
            line_sgst = Decimal("0")
            line_igst = Decimal("0")
            
            if tax_treatment == TaxTreatment.GST.value:
                gst_rate = Decimal(str(line_data.get("gst_rate", 0)))
                if is_interstate:
                    line_igst = taxable_value * (gst_rate / Decimal("100"))
                else:
                    half_rate = gst_rate / Decimal("2")
                    line_cgst = taxable_value * (half_rate / Decimal("100"))
                    line_sgst = taxable_value * (half_rate / Decimal("100"))
            
            # Rounding for tax amounts
            line_cgst = line_cgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            line_sgst = line_sgst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            line_igst = line_igst.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            
            line_total = taxable_value + line_cgst + line_sgst + line_igst
            
            subtotal += gross_amount
            discount_total += line_discount
            taxable_total += taxable_value
            cgst_total += line_cgst
            sgst_total += line_sgst
            igst_total += line_igst
            
            calc_line = {
                **line_data,
                "gross_amount": float(gross_amount),
                "taxable_value": float(taxable_value),
                "cgst_amount": float(line_cgst),
                "sgst_amount": float(line_sgst),
                "igst_amount": float(line_igst),
                "cess_amount": 0.0,
                "line_total": float(line_total)
            }
            calculated_lines.append(calc_line)
            
        grand_total = taxable_total + cgst_total + sgst_total + igst_total
        grand_total_rounded = grand_total.quantize(Decimal("1."), rounding=ROUND_HALF_UP)
        round_off = grand_total_rounded - grand_total
        
        amount_in_words_str = amount_in_words(grand_total_rounded)
        
        return {
            "subtotal": float(subtotal),
            "discount_total": float(discount_total),
            "taxable_total": float(taxable_total),
            "cgst_total": float(cgst_total),
            "sgst_total": float(sgst_total),
            "igst_total": float(igst_total),
            "cess_total": 0.0,
            "round_off": float(round_off),
            "grand_total": float(grand_total_rounded),
            "amount_in_words": amount_in_words_str,
            "lines": calculated_lines
        }

    @staticmethod
    def create_order(db: Session, company_id: str, company: Company, data: dict, user_id: str = None) -> SupplyOrder:
        calc_result = OrderService.calculate_order(db, company_id, company, data)
        
        order = SupplyOrder(
            id=str(uuid.uuid4()),
            company_id=company_id,
            party_id=data["party_id"],
            order_type=data["order_type"],
            tax_treatment=data["tax_treatment"],
            order_date=datetime.strptime(data["order_date"], "%Y-%m-%d").date(),
            expected_date=datetime.strptime(data["expected_date"], "%Y-%m-%d").date() if data.get("expected_date") else None,
            place_of_supply=data["place_of_supply"],
            status=OrderStatus.DRAFT,
            revision=1,
            
            subtotal=calc_result["subtotal"],
            discount_total=calc_result["discount_total"],
            taxable_total=calc_result["taxable_total"],
            cgst_total=calc_result["cgst_total"],
            sgst_total=calc_result["sgst_total"],
            igst_total=calc_result["igst_total"],
            cess_total=calc_result["cess_total"],
            other_charges=0,
            round_off=calc_result["round_off"],
            grand_total=calc_result["grand_total"],
            amount_in_words=calc_result["amount_in_words"],
            notes=data.get("notes"),
            terms=data.get("terms")
        )
        
        for line_data in calc_result["lines"]:
            line = SupplyOrderLine(
                id=str(uuid.uuid4()),
                order_id=order.id,
                item_id=line_data.get("item_id"),
                item_name_snapshot=line_data["item_name"],
                sku_snapshot=line_data.get("sku"),
                hsn_sac_snapshot=line_data.get("hsn_sac"),
                unit_id=line_data["unit_id"],
                unit_name_snapshot=line_data["unit_name"],
                unit_symbol_snapshot=line_data["unit_symbol"],
                quantity=line_data["quantity"],
                rate=line_data["rate"],
                discount_type=line_data.get("discount_type", "NONE"),
                discount_value=line_data.get("discount_value", 0),
                tax_treatment=order.tax_treatment,
                gst_rate=line_data.get("gst_rate", 0),
                taxable_value=line_data["taxable_value"],
                cgst_amount=line_data["cgst_amount"],
                sgst_amount=line_data["sgst_amount"],
                igst_amount=line_data["igst_amount"],
                cess_amount=0,
                line_total=line_data["line_total"],
                description=line_data.get("description")
            )
            order.lines.append(line)
            
        db.add(order)
        
        # Handle Quotation linking
        if data.get("quotation_id"):
            quotation = db.query(Quotation).filter(Quotation.id == data["quotation_id"]).first()
            if quotation:
                quotation.fully_converted = True
                
                doc_link = DocumentLink(
                    company_id=company_id,
                    source_type="QUOTATION",
                    source_id=quotation.id,
                    source_revision=quotation.revision,
                    target_type="SUPPLY_ORDER",
                    target_id=order.id,
                    target_revision=1,
                    relationship_type="CONVERTED_TO_ORDER",
                    created_by=user_id
                )
                db.add(doc_link)
                
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order(db: Session, company_id: str, order_id: str) -> SupplyOrder:
        order = db.query(SupplyOrder).filter(
            SupplyOrder.id == order_id, 
            SupplyOrder.company_id == company_id
        ).first()
        if not order:
            raise NotFoundException("Order not found")
        return order

    @staticmethod
    def list_orders(db: Session, company_id: str, order_type: str = None) -> list[SupplyOrder]:
        query = db.query(SupplyOrder).filter(SupplyOrder.company_id == company_id)
        if order_type:
            query = query.filter(SupplyOrder.order_type == order_type)
        return query.order_by(SupplyOrder.created_at.desc()).all()

    @staticmethod
    def confirm_order(db: Session, company_id: str, order_id: str) -> SupplyOrder:
        order = OrderService.get_order(db, company_id, order_id)
        if order.status != OrderStatus.DRAFT:
            raise ValidationException("Only DRAFT orders can be confirmed.")
            
        # In a full system, you would allocate a real order number here
        order.order_number = f"ORD-{datetime.now().strftime('%Y%m')}-{order.id[:6].upper()}"
        order.status = OrderStatus.CONFIRMED
        
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def convert_to_invoice(db: Session, company_id: str, order_id: str) -> Invoice:
        order = OrderService.get_order(db, company_id, order_id)
        if order.status not in [OrderStatus.CONFIRMED, OrderStatus.PARTIALLY_FULFILLED]:
            raise ValidationException("Only confirmed orders can be converted to bills/invoices.")
            
        party = db.query(Party).filter(Party.id == order.party_id).first()
        company = db.query(Company).filter(Company.id == company_id).first()
        
        invoice = Invoice(
            id=str(uuid.uuid4()),
            company_id=company_id,
            invoice_number=f"DRAFT-{str(uuid.uuid4())[:8].upper()}",
            invoice_series="DRAFT",
            invoice_date=datetime.utcnow().date(),
            order_id=order.id,
            transaction_type=order.order_type.value,
            place_of_supply=order.place_of_supply,
            
            subtotal=order.subtotal,
            discount_total=order.discount_total,
            taxable_total=order.taxable_total,
            cgst_total=order.cgst_total,
            sgst_total=order.sgst_total,
            igst_total=order.igst_total,
            cess_total=order.cess_total,
            grand_total=order.grand_total,
            amount_in_words=order.amount_in_words,
            notes=order.notes,
            terms=order.terms,
            invoice_status="DRAFT"
        )
        
        if order.order_type == OrderType.SALES:
            invoice.customer_id = party.id
            invoice.customer_name_snapshot = party.legal_name
            invoice.customer_gstin_snapshot = party.gstin
            invoice.customer_state_code_snapshot = party.state_code
            
            invoice.seller_id = None
            invoice.seller_name_snapshot = company.legal_name
            invoice.seller_gstin_snapshot = company.gstin
            invoice.seller_state_code_snapshot = company.state_code
        else:
            invoice.seller_id = party.id
            invoice.seller_name_snapshot = party.legal_name
            invoice.seller_gstin_snapshot = party.gstin
            invoice.seller_state_code_snapshot = party.state_code
            
            invoice.customer_id = None
            invoice.customer_name_snapshot = company.legal_name
            invoice.customer_gstin_snapshot = company.gstin
            invoice.customer_state_code_snapshot = company.state_code

        for o_line in order.lines:
            unfulfilled = o_line.quantity - o_line.fulfilled_quantity
            if unfulfilled <= 0:
                continue # Skip fully fulfilled lines
                
            line = InvoiceLine(
                id=str(uuid.uuid4()),
                invoice_id=invoice.id,
                item_id=o_line.item_id,
                item_name_snapshot=o_line.item_name_snapshot,
                sku_snapshot=o_line.sku_snapshot,
                hsn_sac_snapshot=o_line.hsn_sac_snapshot,
                quantity=unfulfilled,
                unit_id=o_line.unit_id,
                unit_name_snapshot=o_line.unit_name_snapshot,
                unit_symbol_snapshot=o_line.unit_symbol_snapshot,
                rate=o_line.rate,
                discount_type=o_line.discount_type,
                discount_value=o_line.discount_value,
                gst_rate=o_line.gst_rate,
            )
            # Recalculate line totals for unfulfilled qty
            # For simplicity in this method, we'll just ratio the amounts. In a real system, we should re-run the calculation engine.
            ratio = unfulfilled / o_line.quantity
            line.taxable_value = o_line.taxable_value * ratio
            line.cgst_amount = o_line.cgst_amount * ratio
            line.sgst_amount = o_line.sgst_amount * ratio
            line.igst_amount = o_line.igst_amount * ratio
            line.line_total = o_line.line_total * ratio
            
            invoice.lines.append(line)
            
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
        return invoice
