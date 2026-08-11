from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.invoice import Invoice, InvoiceLine, InvoiceSeries
from app.models.party import Party
from app.models.item import Item
from app.models.unit import Unit
from app.core.exceptions import ValidationException, NotFoundException, InvoiceLockedException
from app.services.audit_service import AuditService
from app.utils.currency import amount_in_words

class InvoiceService:
    @staticmethod
    def create_invoice(db: Session, company_id: str, company, data: dict) -> Invoice:
        # Validate customer
        customer = db.query(Party).filter(
            Party.id == data["customer_id"],
            Party.company_id == company_id
        ).first()
        if not customer:
            raise ValidationException("Customer not found")
        
        # Get or create invoice series
        series = db.query(InvoiceSeries).filter(
            InvoiceSeries.company_id == company_id,
            InvoiceSeries.document_type == data.get("invoice_type", "TAX_INVOICE"),
            InvoiceSeries.status == "ACTIVE"
        ).first()
        
        if not series:
            series = InvoiceSeries(
                company_id=company_id,
                document_type=data.get("invoice_type", "TAX_INVOICE"),
                prefix="INV-",
                starting_number=1,
                current_number=1,
            )
            db.add(series)
            db.flush()
        
        invoice = Invoice(
            company_id=company_id,
            invoice_number=f"DRAFT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            invoice_series=series.prefix,
            invoice_type=data.get("invoice_type", "TAX_INVOICE"),
            invoice_date=data["invoice_date"],
            customer_id=customer.id,
            customer_name_snapshot=customer.legal_name,
            customer_gstin_snapshot=customer.gstin,
            customer_address_snapshot=InvoiceService._format_address(customer),
            customer_state_snapshot=customer.state,
            customer_state_code_snapshot=customer.state_code,
            place_of_supply=data["place_of_supply"],
            seller_name_snapshot=company.company_name,
            seller_gstin_snapshot=company.gst_details.gstin if company.gst_details else None,
            seller_address_snapshot=InvoiceService._format_company_address(company),
            seller_state_snapshot=company.addresses[0].state if company.addresses else None,
            seller_state_code_snapshot=company.addresses[0].state_code if company.addresses else None,
            notes=data.get("notes"),
            terms=data.get("terms"),
            invoice_status="DRAFT",
        )
        db.add(invoice)
        db.flush()
        
        # Process lines
        subtotal = Decimal("0")
        discount_total = Decimal("0")
        taxable_total = Decimal("0")
        cgst_total = Decimal("0")
        sgst_total = Decimal("0")
        igst_total = Decimal("0")
        
        is_interstate = (invoice.seller_state_code_snapshot or "") != (invoice.customer_state_code_snapshot or "")
        
        for line_data in data["lines"]:
            rate = Decimal(str(line_data["rate"]))
            qty = Decimal(str(line_data["quantity"]))
            discount_value = Decimal(str(line_data.get("discount_value", 0)))
            discount_type = line_data.get("discount_type", "NONE")
            gst_rate = Decimal(str(line_data.get("gst_rate", 0)))
            
            gross = (rate * qty).quantize(Decimal("0.01"))
            
            if discount_type == "PERCENT":
                discount_amount = (gross * discount_value / 100).quantize(Decimal("0.01"))
            elif discount_type == "FIXED":
                discount_amount = discount_value.quantize(Decimal("0.01"))
            else:
                discount_amount = Decimal("0")
            
            taxable = (gross - discount_amount).quantize(Decimal("0.01"))
            tax_amount = (taxable * gst_rate / 100).quantize(Decimal("0.01"))
            
            cgst_amount = Decimal("0")
            sgst_amount = Decimal("0")
            igst_amount = Decimal("0")
            
            if is_interstate:
                igst_amount = tax_amount
            else:
                cgst_amount = (tax_amount / 2).quantize(Decimal("0.01"))
                sgst_amount = (tax_amount / 2).quantize(Decimal("0.01"))
            
            line_total = (taxable + cgst_amount + sgst_amount + igst_amount).quantize(Decimal("0.01"))
            
            line = InvoiceLine(
                invoice_id=invoice.id,
                item_id=line_data.get("item_id"),
                item_name_snapshot=line_data["item_name"],
                sku_snapshot=line_data.get("sku"),
                description_snapshot=line_data.get("description"),
                hsn_sac_snapshot=line_data.get("hsn_sac"),
                quantity=qty,
                unit_id=line_data.get("unit_id"),
                unit_name_snapshot=line_data.get("unit_name"),
                unit_symbol_snapshot=line_data.get("unit_symbol"),
                rate=rate,
                discount_type=discount_type,
                discount_value=discount_value,
                discount_amount=discount_amount,
                taxable_value=taxable,
                gst_rate=gst_rate,
                cgst_rate=gst_rate / 2 if not is_interstate else Decimal("0"),
                sgst_rate=gst_rate / 2 if not is_interstate else Decimal("0"),
                igst_rate=gst_rate if is_interstate else Decimal("0"),
                cgst_amount=cgst_amount,
                sgst_amount=sgst_amount,
                igst_amount=igst_amount,
                line_total=line_total,
            )
            db.add(line)
            
            subtotal += gross
            discount_total += discount_amount
            taxable_total += taxable
            cgst_total += cgst_amount
            sgst_total += sgst_amount
            igst_total += igst_amount
        
        round_off = Decimal("0")
        grand_total = (taxable_total + cgst_total + sgst_total + igst_total).quantize(Decimal("0.01"))
        
        invoice.subtotal = subtotal
        invoice.discount_total = discount_total
        invoice.taxable_total = taxable_total
        invoice.cgst_total = cgst_total
        invoice.sgst_total = sgst_total
        invoice.igst_total = igst_total
        invoice.grand_total = grand_total
        invoice.amount_in_words = amount_in_words(float(grand_total))
        
        db.commit()
        db.refresh(invoice)
        AuditService.log(db, company_id, "INVOICE", invoice.id, "CREATED")
        return invoice
    
    @staticmethod
    def finalize_invoice(db: Session, company_id: str, invoice_id: str) -> Invoice:
        invoice = db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.company_id == company_id
        ).first()
        if not invoice:
            raise NotFoundException("Invoice not found")
        if invoice.invoice_status != "DRAFT":
            raise ValidationException("Only draft invoices can be finalized")
        
        # Get series and assign number atomically
        series = db.query(InvoiceSeries).filter(
            InvoiceSeries.company_id == company_id,
            InvoiceSeries.prefix == invoice.invoice_series
        ).with_for_update().first()
        
        if not series:
            raise ValidationException("Invoice series not found")
        
        invoice_number = f"{series.prefix}{series.current_number:06d}"
        series.current_number += 1
        
        invoice.invoice_number = invoice_number
        invoice.invoice_status = "FINALIZED"
        invoice.finalized_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(invoice)
        AuditService.log(db, company_id, "INVOICE", invoice.id, "FINALIZED")
        return invoice
    
    @staticmethod
    def cancel_invoice(db: Session, company_id: str, invoice_id: str, reason: str):
        invoice = db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.company_id == company_id
        ).first()
        if not invoice:
            raise NotFoundException("Invoice not found")
        if invoice.invoice_status != "FINALIZED":
            raise ValidationException("Only finalized invoices can be cancelled")
        
        invoice.invoice_status = "CANCELLED"
        db.commit()
        AuditService.log(db, company_id, "INVOICE", invoice.id, "CANCELLED", reason=reason)
        return invoice
    
    @staticmethod
    def list_invoices(db: Session, company_id: str, status: str = None):
        query = db.query(Invoice).filter(Invoice.company_id == company_id)
        if status:
            query = query.filter(Invoice.invoice_status == status)
        return query.order_by(Invoice.created_at.desc()).all()
    
    @staticmethod
    def get_invoice(db: Session, company_id: str, invoice_id: str):
        invoice = db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.company_id == company_id
        ).first()
        if not invoice:
            raise NotFoundException("Invoice not found")
        return invoice
    
    @staticmethod
    def _format_address(party: Party) -> str:
        parts = []
        if party.addresses:
            addr = party.addresses[0]
            parts = [addr.address_line_1, addr.city, addr.state, addr.pincode]
        return ", ".join([p for p in parts if p])
    
    @staticmethod
    def _format_company_address(company) -> str:
        parts = []
        if company.addresses:
            addr = company.addresses[0]
            parts = [addr.address_line_1, addr.city, addr.state, addr.pincode]
        return ", ".join([p for p in parts if p])
