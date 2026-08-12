from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceListResponse, InvoiceFinalizeRequest, InvoiceCancelRequest, InvoiceCalculateRequest, InvoiceCalculateResponse
from app.services.invoice_service import InvoiceService
from app.services.pdf_service import PdfService

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/calculate", response_model=ApiResponse[InvoiceCalculateResponse])
def calculate_invoice(request: InvoiceCalculateRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    result = InvoiceService.calculate_invoice(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=InvoiceCalculateResponse(**result))

@router.post("/", response_model=ApiResponse[InvoiceResponse])
def create_invoice(request: InvoiceCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.create_invoice(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=_invoice_to_response(invoice))

@router.get("/", response_model=ApiResponse[InvoiceListResponse])
def list_invoices(status: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoices = InvoiceService.list_invoices(db, str(company.id), status)
    return ApiResponse(success=True, data=InvoiceListResponse(
        items=[_invoice_to_response(i) for i in invoices],
        total=len(invoices)
    ))

@router.get("/{invoice_id}", response_model=ApiResponse[InvoiceResponse])
def get_invoice(invoice_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.get_invoice(db, str(company.id), invoice_id)
    return ApiResponse(success=True, data=_invoice_to_response(invoice))

@router.get("/{invoice_id}/pdf")
def get_invoice_pdf(invoice_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.get_invoice(db, str(company.id), invoice_id)
    pdf_bytes = PdfService.generate_invoice_pdf(invoice)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=invoice_{invoice.invoice_number}.pdf"
        }
    )

@router.post("/{invoice_id}/finalize", response_model=ApiResponse[InvoiceResponse])
def finalize_invoice(invoice_id: str, request: InvoiceFinalizeRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.finalize_invoice(db, str(company.id), invoice_id)
    return ApiResponse(success=True, data=_invoice_to_response(invoice))

@router.post("/{invoice_id}/cancel", response_model=ApiResponse[InvoiceResponse])
def cancel_invoice(invoice_id: str, request: InvoiceCancelRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.cancel_invoice(db, str(company.id), invoice_id, request.reason)
    return ApiResponse(success=True, data=_invoice_to_response(invoice))

def _invoice_to_response(invoice) -> InvoiceResponse:
    return InvoiceResponse(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_type=invoice.invoice_type,
        invoice_date=invoice.invoice_date.date(),
        customer_name_snapshot=invoice.customer_name_snapshot,
        customer_gstin_snapshot=invoice.customer_gstin_snapshot,
        place_of_supply=invoice.place_of_supply,
        subtotal=float(invoice.subtotal),
        discount_total=float(invoice.discount_total),
        taxable_total=float(invoice.taxable_total),
        cgst_total=float(invoice.cgst_total),
        sgst_total=float(invoice.sgst_total),
        igst_total=float(invoice.igst_total),
        grand_total=float(invoice.grand_total),
        amount_in_words=invoice.amount_in_words,
        invoice_status=invoice.invoice_status,
        payment_status=invoice.payment_status,
        notes=invoice.notes,
        lines=[{
            "id": l.id,
            "item_name": l.item_name_snapshot,
            "description": l.description_snapshot,
            "hsn_sac_snapshot": l.hsn_sac_snapshot,
            "quantity": float(l.quantity),
            "unit_name_snapshot": l.unit_name_snapshot,
            "unit_symbol_snapshot": l.unit_symbol_snapshot,
            "rate": float(l.rate),
            "discount_amount": float(l.discount_amount),
            "taxable_value": float(l.taxable_value),
            "gst_rate": float(l.gst_rate),
            "cgst_amount": float(l.cgst_amount),
            "sgst_amount": float(l.sgst_amount),
            "igst_amount": float(l.igst_amount),
            "line_total": float(l.line_total),
        } for l in invoice.lines],
        created_at=invoice.created_at,
    )
