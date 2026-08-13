from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.order import (
    SupplyOrderCreate, SupplyOrderResponse, SupplyOrderListResponse, 
    SupplyOrderCalculateRequest, SupplyOrderCalculateResponse, SupplyOrderLineResponse
)
from app.schemas.invoice import InvoiceResponse
from app.services.order_service import OrderService
from app.api.v1.invoices import _invoice_to_response
from typing import Optional

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/calculate", response_model=ApiResponse[SupplyOrderCalculateResponse])
def calculate_order(request: SupplyOrderCalculateRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    result = OrderService.calculate_order(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=SupplyOrderCalculateResponse(**result))

@router.post("/", response_model=ApiResponse[SupplyOrderResponse])
def create_order(request: SupplyOrderCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    order = OrderService.create_order(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=_order_to_response(order))

@router.get("/", response_model=ApiResponse[SupplyOrderListResponse])
def list_orders(
    order_type: Optional[str] = Query(None),
    company = Depends(get_current_company), 
    db: Session = Depends(get_db)
):
    orders = OrderService.list_orders(db, str(company.id), order_type)
    return ApiResponse(success=True, data=SupplyOrderListResponse(
        items=[_order_to_response(o) for o in orders],
        total=len(orders)
    ))

@router.get("/{order_id}", response_model=ApiResponse[SupplyOrderResponse])
def get_order(order_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    order = OrderService.get_order(db, str(company.id), order_id)
    return ApiResponse(success=True, data=_order_to_response(order))

@router.post("/{order_id}/confirm", response_model=ApiResponse[SupplyOrderResponse])
def confirm_order(order_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    order = OrderService.confirm_order(db, str(company.id), order_id)
    return ApiResponse(success=True, data=_order_to_response(order))

@router.post("/{order_id}/convert", response_model=ApiResponse[InvoiceResponse])
def convert_to_invoice(order_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = OrderService.convert_to_invoice(db, str(company.id), order_id)
    return ApiResponse(success=True, data=_invoice_to_response(invoice))


def _order_to_response(order) -> SupplyOrderResponse:
    lines = []
    for line in order.lines:
        lines.append(SupplyOrderLineResponse(
            id=line.id,
            item_id=line.item_id,
            item_name_snapshot=line.item_name_snapshot,
            sku_snapshot=line.sku_snapshot,
            hsn_sac_snapshot=line.hsn_sac_snapshot,
            unit_id=line.unit_id,
            unit_name_snapshot=line.unit_name_snapshot,
            unit_symbol_snapshot=line.unit_symbol_snapshot,
            quantity=float(line.quantity),
            fulfilled_quantity=float(line.fulfilled_quantity),
            rate=float(line.rate),
            discount_type=line.discount_type,
            discount_value=float(line.discount_value),
            tax_treatment=line.tax_treatment.value,
            gst_rate=float(line.gst_rate),
            taxable_value=float(line.taxable_value),
            cgst_amount=float(line.cgst_amount),
            sgst_amount=float(line.sgst_amount),
            igst_amount=float(line.igst_amount),
            cess_amount=float(line.cess_amount),
            line_total=float(line.line_total),
            description=line.description
        ))
        
    return SupplyOrderResponse(
        id=order.id,
        order_type=order.order_type.value,
        tax_treatment=order.tax_treatment.value,
        order_number=order.order_number,
        order_date=order.order_date,
        expected_date=order.expected_date,
        party_id=order.party_id,
        place_of_supply=order.place_of_supply,
        status=order.status.value,
        revision=order.revision,
        subtotal=float(order.subtotal),
        discount_total=float(order.discount_total),
        taxable_total=float(order.taxable_total),
        cgst_total=float(order.cgst_total),
        sgst_total=float(order.sgst_total),
        igst_total=float(order.igst_total),
        cess_total=float(order.cess_total),
        other_charges=float(order.other_charges),
        round_off=float(order.round_off),
        grand_total=float(order.grand_total),
        amount_in_words=order.amount_in_words,
        notes=order.notes,
        terms=order.terms,
        lines=lines
    )
