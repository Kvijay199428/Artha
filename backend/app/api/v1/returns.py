from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.return_order import (
    ReturnOrderCreate, ReturnOrderResponse, ReturnOrderListResponse, 
    ReturnableLinesResponse, ReturnSettlementCreate, ReturnSettlementResponse
)
from app.services.return_service import ReturnService

router = APIRouter(prefix="/returns", tags=["Returns"])

@router.get("/order/{order_id}/returnable-lines", response_model=ApiResponse[ReturnableLinesResponse])
def get_returnable_lines(order_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    data = ReturnService.get_returnable_lines(db, str(company.id), order_id)
    return ApiResponse(success=True, data=ReturnableLinesResponse(**data))

@router.post("/", response_model=ApiResponse[ReturnOrderResponse])
def create_return(request: ReturnOrderCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    ret = ReturnService.create_return(db, str(company.id), request.model_dump(), None)
    return ApiResponse(success=True, data=_return_to_response(ret))

@router.get("/", response_model=ApiResponse[ReturnOrderListResponse])
def list_returns(return_type: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    returns = ReturnService.list_returns(db, str(company.id), return_type)
    return ApiResponse(success=True, data=ReturnOrderListResponse(
        items=[_return_to_response(r) for r in returns],
        total=len(returns)
    ))

@router.get("/{return_id}", response_model=ApiResponse[ReturnOrderResponse])
def get_return(return_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    ret = ReturnService.get_return(db, str(company.id), return_id)
    return ApiResponse(success=True, data=_return_to_response(ret))

@router.post("/{return_id}/approve", response_model=ApiResponse[ReturnOrderResponse])
def approve_return(return_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    ret = ReturnService.approve_return(db, str(company.id), return_id, None)
    return ApiResponse(success=True, data=_return_to_response(ret))

@router.post("/{return_id}/post", response_model=ApiResponse[ReturnOrderResponse])
def post_return(return_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    ret = ReturnService.post_return(db, str(company.id), return_id)
    return ApiResponse(success=True, data=_return_to_response(ret))

@router.post("/{return_id}/adjust-receivable", response_model=ApiResponse[ReturnSettlementResponse])
def adjust_receivable(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "ADJUST_RECEIVABLE"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/adjust-payable", response_model=ApiResponse[ReturnSettlementResponse])
def adjust_payable(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "ADJUST_PAYABLE"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/customer-refund", response_model=ApiResponse[ReturnSettlementResponse])
def customer_refund(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "CUSTOMER_REFUND"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/supplier-refund", response_model=ApiResponse[ReturnSettlementResponse])
def supplier_refund(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "SUPPLIER_REFUND"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/customer-credit", response_model=ApiResponse[ReturnSettlementResponse])
def customer_credit(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "CUSTOMER_CREDIT"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/supplier-credit", response_model=ApiResponse[ReturnSettlementResponse])
def supplier_credit(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    request.settlement_type = "SUPPLIER_CREDIT"
    return _process_settlement(db, str(company.id), return_id, request)

@router.post("/{return_id}/settlements", response_model=ApiResponse[ReturnSettlementResponse])
def add_settlement(return_id: str, request: ReturnSettlementCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    return _process_settlement(db, str(company.id), return_id, request)

def _process_settlement(db: Session, company_id: str, return_id: str, request: ReturnSettlementCreate):
    settlement = ReturnService.add_settlement(db, company_id, return_id, request.model_dump())
    return ApiResponse(success=True, data=ReturnSettlementResponse(
        id=settlement.id,
        settlement_type=settlement.settlement_type.value,
        amount=float(settlement.amount),
        status=settlement.status,
        settlement_date=settlement.settlement_date,
        reference_number=settlement.reference_number,
        notes=settlement.notes
    ))

def _return_to_response(ret) -> ReturnOrderResponse:
    lines = []
    for l in ret.lines:
        lines.append({
            "id": l.id,
            "original_order_line_id": l.original_order_line_id,
            "item_id": l.item_id,
            "item_name_snapshot": l.item_name_snapshot,
            "sku_snapshot": l.sku_snapshot,
            "hsn_sac_snapshot": l.hsn_sac_snapshot,
            "unit_snapshot": l.unit_snapshot,
            "original_quantity": float(l.original_quantity),
            "previously_returned_quantity": float(l.previously_returned_quantity),
            "return_quantity": float(l.return_quantity),
            "remaining_quantity": float(l.remaining_quantity),
            "rate": float(l.rate),
            "taxable_value": float(l.taxable_value),
            "gst_rate": float(l.gst_rate),
            "cgst_amount": float(l.cgst_amount),
            "sgst_amount": float(l.sgst_amount),
            "igst_amount": float(l.igst_amount),
            "line_total": float(l.line_total),
            "condition": l.condition.value,
            "warehouse_action": l.warehouse_action.value
        })
        
    settlements = []
    for s in ret.settlements:
        settlements.append({
            "id": s.id,
            "settlement_type": s.settlement_type.value,
            "amount": float(s.amount),
            "status": s.status,
            "settlement_date": s.settlement_date,
            "reference_number": s.reference_number,
            "notes": s.notes
        })
        
    return ReturnOrderResponse(
        id=ret.id,
        return_number=ret.return_number,
        return_type=ret.return_type.value,
        original_order_id=ret.original_order_id,
        party_id=ret.party_id,
        return_date=ret.return_date.date(),
        status=ret.status.value,
        financial_status=ret.financial_status.value,
        reason=ret.reason,
        subtotal=float(ret.subtotal),
        discount_total=float(ret.discount_total),
        taxable_total=float(ret.taxable_total),
        cgst_total=float(ret.cgst_total),
        sgst_total=float(ret.sgst_total),
        igst_total=float(ret.igst_total),
        grand_total=float(ret.grand_total),
        created_at=ret.created_at,
        lines=lines,
        settlements=settlements
    )
