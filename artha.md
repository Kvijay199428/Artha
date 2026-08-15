```
// File: backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies using pip and pyproject.toml
COPY pyproject.toml ./
RUN pip install --no-cache-dir .

COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```ini
// File: backend/alembic.ini
[alembic]
script_location = migrations
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = sqlite:///./data/artha.db

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

```python
// File: backend/app/__init__.py

```

```python
// File: backend/app/api/__init__.py

```

```python
// File: backend/app/api/v1/__init__.py
from fastapi import APIRouter
from app.api.v1 import auth, company, units, items, parties, invoices, master, orders, returns, quotations, boq, estimates, gst, adjustments, documents

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(company.router)
api_router.include_router(units.router)
api_router.include_router(items.router)
api_router.include_router(parties.router)
api_router.include_router(invoices.router)
api_router.include_router(master.router)
api_router.include_router(orders.router)
api_router.include_router(returns.router)
api_router.include_router(quotations.router)
api_router.include_router(boq.router)
api_router.include_router(estimates.router)
api_router.include_router(gst.router)
api_router.include_router(adjustments.router)
api_router.include_router(documents.router)
```

```python
// File: backend/app/api/v1/adjustments.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas.adjustment import AdjustmentNoteCreate, AdjustmentNoteResponse, AdjustmentNoteListResponse, NoteAllocationCreate, NoteAllocationResponse
from app.schemas.common import ApiResponse
from app.services.adjustment import FinancialAdjustmentService
from app.dependencies.auth import get_current_company

router = APIRouter(prefix="/adjustment-notes", tags=["Adjustments"])

@router.get("", response_model=ApiResponse[AdjustmentNoteListResponse])
def get_adjustment_notes(
    *,
    db: Session = Depends(get_db),
    note_type: Optional[str] = None,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    items, total = service.get_notes(company_id=current_company.id, note_type=note_type)
    return ApiResponse(success=True, data=AdjustmentNoteListResponse(items=items, total=total))

@router.post("", response_model=ApiResponse[AdjustmentNoteResponse])
def create_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_in: AdjustmentNoteCreate,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    if note_in.note_type == "CREDIT_NOTE":
        note = service.create_credit_note(note_in=note_in, company_id=current_company.id)
    else:
        note = service.create_debit_note(note_in=note_in, company_id=current_company.id)
    return ApiResponse(success=True, data=note)

@router.get("/{note_id}", response_model=ApiResponse[AdjustmentNoteResponse])
def get_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.get_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/post", response_model=ApiResponse[AdjustmentNoteResponse])
def post_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.post_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/approve", response_model=ApiResponse[AdjustmentNoteResponse])
def approve_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.approve_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/cancel", response_model=ApiResponse[AdjustmentNoteResponse])
def cancel_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.cancel_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.post("/{note_id}/reverse", response_model=ApiResponse[AdjustmentNoteResponse])
def reverse_adjustment_note(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    service = FinancialAdjustmentService(db)
    note = service.reverse_note(note_id=note_id, company_id=current_company.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return ApiResponse(success=True, data=note)

@router.get("/{note_id}/pdf")
def get_adjustment_note_pdf(
    *,
    db: Session = Depends(get_db),
    note_id: str,
    current_company = Depends(get_current_company)
):
    raise HTTPException(status_code=501, detail="PDF generation not implemented yet")
```

```python
// File: backend/app/api/v1/auth.py
import time
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.exceptions import ValidationException
from app.schemas.auth import CompanySetupRequest, LoginRequest, LoginResponse, CompanyProfileResponse
from app.schemas.common import ApiResponse
from app.services.company_service import CompanyService
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_company

router = APIRouter(prefix="/auth", tags=["Authentication"])

class PinResetRequest(BaseModel):
    old_pin: str
    new_pin: str
    confirm_pin: str

@router.post("/setup", response_model=ApiResponse[CompanyProfileResponse])
def setup_company(request: CompanySetupRequest, db: Session = Depends(get_db)):
    company = CompanyService.create_company(db, request)
    time.sleep(5)  # 5-second backend artificial delay
    return ApiResponse(success=True, data=CompanyProfileResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile=company.mobile,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        logo_url=None
    ))

@router.post("/login", response_model=ApiResponse[LoginResponse])
def login(request: LoginRequest, db: Session = Depends(get_db)):
    # For simplicity, we assume single company mode for now
    from app.models.company import Company
    company = db.query(Company).first()
    if not company:
        raise ValidationException("No company found. Please complete setup first.")
    
    token = AuthService.authenticate(db, company.id, request.pin)
    time.sleep(5)  # 5-second backend artificial delay
    return ApiResponse(success=True, data=LoginResponse(
        token=token,
        company_name=company.company_name,
        company_id=company.id
    ))

@router.get("/me", response_model=ApiResponse[CompanyProfileResponse])
def get_me(company = Depends(get_current_company)):
    return ApiResponse(success=True, data=CompanyProfileResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile=company.mobile,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        logo_url=None
    ))

@router.post("/pin-change", response_model=ApiResponse[bool])
def change_pin(
    request: PinResetRequest,
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    if request.new_pin != request.confirm_pin:
        raise ValidationException("New PIN and confirm PIN do not match")
    CompanyService.change_pin(db, company.id, request.old_pin, request.new_pin)
    return ApiResponse(success=True, data=True)

@router.post("/logout", response_model=ApiResponse[bool])
def logout(
    request: Request,
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        AuthService.logout(db, token)
    return ApiResponse(success=True, data=True)
```

```python
// File: backend/app/api/v1/boq.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.boq import BOQCreate, BOQResponse, BOQListResponse
from app.services.boq_service import BOQService

router = APIRouter(prefix="/boqs", tags=["BOQ"])

@router.post("/", response_model=ApiResponse[BOQResponse])
def create_boq(request: BOQCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    boq = BOQService.create_boq(db, str(company.id), request.model_dump(), None)
    return ApiResponse(success=True, data=_boq_to_response(boq))

@router.get("/", response_model=ApiResponse[BOQListResponse])
def list_boqs(company = Depends(get_current_company), db: Session = Depends(get_db)):
    boqs = BOQService.list_boqs(db, str(company.id))
    return ApiResponse(success=True, data=BOQListResponse(
        items=[_boq_to_response(b) for b in boqs],
        total=len(boqs)
    ))

@router.get("/{boq_id}", response_model=ApiResponse[BOQResponse])
def get_boq(boq_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    boq = BOQService.get_boq(db, str(company.id), boq_id)
    return ApiResponse(success=True, data=_boq_to_response(boq))

@router.post("/{boq_id}/approve", response_model=ApiResponse[BOQResponse])
def approve_boq(boq_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    boq = BOQService.approve_boq(db, str(company.id), boq_id)
    return ApiResponse(success=True, data=_boq_to_response(boq))

def _boq_to_response(boq) -> BOQResponse:
    lines = []
    for l in boq.lines:
        lines.append({
            "id": l.id,
            "parent_line_id": l.parent_line_id,
            "section": l.section,
            "item_type": l.item_type.value,
            "item_id": l.item_id,
            "description": l.description,
            "specification": l.specification,
            "quantity": float(l.quantity),
            "unit_id": l.unit_id,
            "unit_snapshot": l.unit_snapshot,
            "quantity_formula": l.quantity_formula,
            "estimated_rate": float(l.estimated_rate),
            "estimated_amount": float(l.estimated_amount),
            "remarks": l.remarks,
            "sort_order": l.sort_order
        })
        
    return BOQResponse(
        id=boq.id,
        boq_number=boq.boq_number,
        project_name=boq.project_name,
        party_id=boq.party_id,
        boq_date=boq.boq_date,
        version=boq.version,
        status=boq.status.value,
        notes=boq.notes,
        created_at=boq.created_at,
        updated_at=boq.updated_at,
        lines=lines
    )
```

```python
// File: backend/app/api/v1/company.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.company import CompanyDetailResponse, CompanyUpdate, CompanyLogoResponse
from app.services.company_service import CompanyService
from fastapi import UploadFile, File

router = APIRouter(prefix="/company", tags=["Company"])

@router.get("/", response_model=ApiResponse[CompanyDetailResponse])
def get_company(company = Depends(get_current_company), db: Session = Depends(get_db)):
    from app.models.company import CompanyGSTDetail
    gst = db.query(CompanyGSTDetail).filter(CompanyGSTDetail.company_id == company.id).first()
    
    addresses = [{
        "id": a.id,
        "address_type": a.address_type,
        "address_line_1": a.address_line_1,
        "address_line_2": a.address_line_2,
        "city": a.city,
        "district": a.district,
        "state": a.state,
        "state_code": a.state_code,
        "pincode": a.pincode,
        "country": a.country,
        "is_default": a.is_default,
    } for a in company.addresses]
    
    banks = [{
        "id": b.id,
        "account_holder_name": b.account_holder_name,
        "account_number": b.account_number,
        "ifsc": b.ifsc,
        "bank_name": b.bank_name,
        "branch": b.branch,
        "account_type": b.account_type,
        "is_primary": b.is_primary,
    } for b in company.bank_accounts]
    
    return ApiResponse(success=True, data=CompanyDetailResponse(
        id=company.id,
        company_name=company.company_name,
        legal_name=company.legal_name,
        trade_name=company.trade_name,
        ownership_type=company.ownership_type,
        status=company.status,
        mobile_country_code=company.mobile_country_code,
        mobile=company.mobile,
        mobile_e164=company.mobile_e164,
        office_phone_country_code=company.office_phone_country_code,
        office_phone=company.office_phone,
        office_phone_e164=company.office_phone_e164,
        email=company.email,
        website=company.website,
        logo_url=company.logo_url,
        authorized_person_name=company.authorized_person_name,
        authorized_person_designation=company.authorized_person_designation,
        gst_details={
            "id": gst.id,
            "gstin": gst.gstin,
            "state_code": gst.state_code,
            "state_name": gst.state_name,
            "pan": gst.pan,
            "tan": gst.tan,
            "gstin_validation_status": gst.gstin_validation_status,
        } if gst else None,
        addresses=addresses,
        bank_accounts=banks,
        created_at=company.created_at,
        updated_at=company.updated_at,
    ))

@router.put("/", response_model=ApiResponse[CompanyDetailResponse])
def update_company(
    data: CompanyUpdate,
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    updated = CompanyService.update_company(db, company.id, data.model_dump(exclude_unset=True))
    return get_company(company=updated, db=db)

@router.post("/logo", response_model=ApiResponse[CompanyLogoResponse])
async def upload_company_logo(
    file: UploadFile = File(...),
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    from app.services.file_storage_service import FileStorageService
    logo_metadata = await FileStorageService.save_company_logo(company.id, file)
    company = CompanyService.update_company_logo(db, company.id, logo_metadata)
    return ApiResponse(success=True, data=CompanyLogoResponse(logo_url=company.logo_url, asset_id=company.logo_asset_id))

@router.delete("/logo", response_model=ApiResponse[bool])
def delete_company_logo(
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    CompanyService.update_company_logo(db, company.id, None)
    return ApiResponse(success=True, data=True)

@router.get("/logo/{company_id}")
def get_company_logo_public(company_id: str, db: Session = Depends(get_db)):
    from fastapi.responses import FileResponse
    from app.models.company import CompanyAsset
    asset = db.query(CompanyAsset).filter(CompanyAsset.company_id == company_id, CompanyAsset.asset_type == "COMPANY_LOGO").order_by(CompanyAsset.created_at.desc()).first()
    if not asset:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Logo not found")
    from app.services.file_storage_service import FileStorageService
    file_path = FileStorageService.get_file_path(asset.file_path)
    return FileResponse(file_path, media_type=asset.mime_type)

@router.get("/logo")
def get_company_logo(company = Depends(get_current_company), db: Session = Depends(get_db)):
    return get_company_logo_public(company.id, db)
```

```python
// File: backend/app/api/v1/documents.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
# Use models and schemas

router = APIRouter()

@router.get("/search")
def search_documents(q: str, db: Session = Depends(get_db)):
    # Search logic across invoices, notes, quotes, etc. based on `q`
    return {"results": []}
```

```python
// File: backend/app/api/v1/estimates.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.estimate import EstimateCreate, EstimateResponse, EstimateListResponse
from app.services.estimate_service import EstimateService

router = APIRouter(prefix="/estimates", tags=["Estimates"])

@router.post("/", response_model=ApiResponse[EstimateResponse])
def create_estimate(request: EstimateCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.create_estimate(db, str(company.id), request.model_dump(), None)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

@router.get("/", response_model=ApiResponse[EstimateListResponse])
def list_estimates(company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimates = EstimateService.list_estimates(db, str(company.id))
    return ApiResponse(success=True, data=EstimateListResponse(
        items=[_estimate_to_response(e) for e in estimates],
        total=len(estimates)
    ))

@router.get("/{estimate_id}", response_model=ApiResponse[EstimateResponse])
def get_estimate(estimate_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.get_estimate(db, str(company.id), estimate_id)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

@router.post("/{estimate_id}/approve", response_model=ApiResponse[EstimateResponse])
def approve_estimate(estimate_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    estimate = EstimateService.approve_estimate(db, str(company.id), estimate_id)
    return ApiResponse(success=True, data=_estimate_to_response(estimate))

def _estimate_to_response(estimate) -> EstimateResponse:
    lines = []
    for l in estimate.lines:
        lines.append({
            "id": l.id,
            "item_name_snapshot": l.item_name_snapshot,
            "item_type": l.item_type,
            "quantity": float(l.quantity),
            "unit_snapshot": l.unit_snapshot,
            "cost_rate": float(l.cost_rate),
            "cost_amount": float(l.cost_amount),
            "markup_percent": float(l.markup_percent),
            "markup_amount": float(l.markup_amount),
            "selling_rate": float(l.selling_rate),
            "selling_amount": float(l.selling_amount)
        })
        
    return EstimateResponse(
        id=estimate.id,
        estimate_number=estimate.estimate_number,
        boq_id=estimate.boq_id,
        party_id=estimate.party_id,
        estimate_date=estimate.estimate_date,
        valid_until=estimate.valid_until,
        version=estimate.version,
        status=estimate.status.value,
        material_cost=float(estimate.material_cost),
        labour_cost=float(estimate.labour_cost),
        service_cost=float(estimate.service_cost),
        other_cost=float(estimate.other_cost),
        total_cost=float(estimate.total_cost),
        markup_amount=float(estimate.markup_amount),
        estimated_selling_value=float(estimate.estimated_selling_value),
        gst_total=float(estimate.gst_total),
        grand_total=float(estimate.grand_total),
        created_at=estimate.created_at,
        updated_at=estimate.updated_at,
        lines=lines
    )
```

```python
// File: backend/app/api/v1/gst.py
from fastapi import APIRouter
from app.core.gst import GSTService
from app.core.gst.schemas import GSTINValidationResult, GSTStateResponse
from app.core.gst.state_codes import GSTStateMaster
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/gst", tags=["GST"])

@router.get("/validate/{gstin}")
def validate_gstin(gstin: str) -> ApiResponse[GSTINValidationResult]:
    result = GSTService.validate(gstin)
    return ApiResponse(success=True, data=result)

@router.get("/states")
def list_states() -> ApiResponse[list[GSTStateResponse]]:
    states = GSTStateMaster.all_states()
    return ApiResponse(success=True, data=[GSTStateResponse(**s) for s in states])

@router.get("/states/{code}")
def get_state(code: str) -> ApiResponse[GSTStateResponse | None]:
    state = GSTStateMaster.get_state(code)
    if not state:
        return ApiResponse(success=False, data=None)
    return ApiResponse(success=True, data=GSTStateResponse(**state))
```

```python
// File: backend/app/api/v1/invoices.py
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

@router.get("/{invoice_id}/relations")
def get_invoice_relations(invoice_id: str, db: Session = Depends(get_db)):
    # Return document links involving this invoice ID
    return {
        "invoice": invoice_id,
        "ancestors": [],
        "children": [],
        "payments": [],
        "returns": [],
        "credit_notes": [],
        "debit_notes": []
    }

@router.get("/{invoice_id}/timeline")
def get_invoice_timeline(invoice_id: str, db: Session = Depends(get_db)):
    # Compile chronological events
    return {"timeline": []}

@router.post("/calculate", response_model=ApiResponse[InvoiceCalculateResponse])
def calculate_invoice(request: InvoiceCalculateRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    result = InvoiceService.calculate_invoice(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=InvoiceCalculateResponse(**result))

@router.post("/", response_model=ApiResponse[InvoiceResponse])
def create_invoice(request: InvoiceCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    invoice = InvoiceService.create_invoice(db, str(company.id), company, request.model_dump())
    return ApiResponse(success=True, data=_invoice_to_response(invoice))

@router.get("/", response_model=ApiResponse[InvoiceListResponse])
def list_invoices(
    status: str = Query(None), 
    transaction_type: str = Query(None),
    company = Depends(get_current_company), 
    db: Session = Depends(get_db)
):
    invoices = InvoiceService.list_invoices(db, str(company.id), status, transaction_type)
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
        transaction_type=invoice.transaction_type,
        invoice_date=invoice.invoice_date.date(),
        customer_name_snapshot=invoice.customer_name_snapshot if invoice.transaction_type == "SALES" else invoice.seller_name_snapshot,
        customer_gstin_snapshot=invoice.customer_gstin_snapshot if invoice.transaction_type == "SALES" else invoice.seller_gstin_snapshot,
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
```

```python
// File: backend/app/api/v1/items.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ApiResponse[ItemResponse])
def create_item(request: ItemCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    item = ItemService.create_item(db, str(company.id), request.model_dump())
    return ApiResponse(success=True, data=ItemResponse(**item))

@router.get("/", response_model=ApiResponse[ItemListResponse])
def list_items(search: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    items = ItemService.list_items(db, str(company.id), search)
    return ApiResponse(success=True, data=ItemListResponse(items=[ItemResponse(**i) for i in items]))

@router.get("/{item_id}", response_model=ApiResponse[ItemResponse])
def get_item(item_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    item = ItemService.get_item(db, str(company.id), item_id)
    return ApiResponse(success=True, data=ItemResponse(**item))

@router.put("/{item_id}", response_model=ApiResponse[ItemResponse])
def update_item(item_id: str, request: ItemUpdate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    item = ItemService.update_item(db, str(company.id), item_id, request.model_dump(exclude_unset=True))
    return ApiResponse(success=True, data=ItemResponse(**item))

@router.delete("/{item_id}", response_model=ApiResponse[dict])
def delete_item(item_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    ItemService.delete_item(db, str(company.id), item_id)
    return ApiResponse(success=True, data={"message": "Item archived"})
```

```python
// File: backend/app/api/v1/master.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.models.master import GSTStateCode, GSTRate

router = APIRouter(prefix="/master", tags=["Master Data"])

@router.get("/gst-states", response_model=ApiResponse[list[dict]])
def get_gst_states(db: Session = Depends(get_db)):
    states = db.query(GSTStateCode).order_by(GSTStateCode.code).all()
    return ApiResponse(success=True, data=[{
        "id": s.id,
        "code": s.code,
        "state_name": s.state_name,
        "union_territory": s.union_territory,
    } for s in states])

@router.get("/gst-rates", response_model=ApiResponse[list[dict]])
def get_gst_rates(db: Session = Depends(get_db)):
    rates = db.query(GSTRate).filter(GSTRate.status == "ACTIVE").order_by(GSTRate.rate).all()
    return ApiResponse(success=True, data=[{
        "id": r.id,
        "rate": float(r.rate),
        "display_name": r.display_name,
        "description": r.description,
    } for r in rates])
```

```python
// File: backend/app/api/v1/orders.py
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
    order = OrderService.create_order(db, str(company.id), company, request.model_dump(), None)
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
```

```python
// File: backend/app/api/v1/parties.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.party import PartyCreate, PartyUpdate, PartyResponse, PartyListResponse
from app.services.party_service import PartyService

router = APIRouter(prefix="/parties", tags=["Parties"])

@router.post("/", response_model=ApiResponse[PartyResponse])
def create_party(request: PartyCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.create_party(db, str(company.id), request.model_dump())
    return ApiResponse(success=True, data=_party_to_response(party))

@router.get("/", response_model=ApiResponse[PartyListResponse])
def list_parties(
    account_type: str = Query(None),
    search: str = Query(None),
    company = Depends(get_current_company),
    db: Session = Depends(get_db)
):
    parties = PartyService.list_parties(db, str(company.id), account_type, search)
    return ApiResponse(success=True, data=PartyListResponse(items=[_party_to_response(p) for p in parties]))

@router.get("/{party_id}", response_model=ApiResponse[PartyResponse])
def get_party(party_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.get_party(db, str(company.id), party_id)
    return ApiResponse(success=True, data=_party_to_response(party))

@router.put("/{party_id}", response_model=ApiResponse[PartyResponse])
def update_party(party_id: str, request: PartyUpdate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    party = PartyService.update_party(db, str(company.id), party_id, request.model_dump(exclude_unset=True))
    return ApiResponse(success=True, data=_party_to_response(party))

def _party_to_response(party) -> PartyResponse:
    return PartyResponse(
        id=party.id,
        company_id=party.company_id,
        party_code=party.party_code,
        legal_name=party.legal_name,
        trade_name=party.trade_name,
        party_type=party.party_type,
        account_type=party.account_type,
        contact_person=party.contact_person,
        mobile=party.mobile,
        email=party.email,
        gstin=party.gstin,
        gst_registration_type=party.gst_registration_type,
        pan=party.pan,
        state=party.state,
        state_code=party.state_code,
        place_of_supply=party.place_of_supply,
        credit_limit=float(party.credit_limit) if party.credit_limit else None,
        credit_days=party.credit_days,
        payment_terms=party.payment_terms,
        notes=party.notes,
        status=party.status,
        created_at=party.created_at,
        updated_at=party.updated_at,
        addresses=[{
            "id": a.id,
            "address_type": a.address_type,
            "address_line_1": a.address_line_1,
            "address_line_2": a.address_line_2,
            "city": a.city,
            "district": a.district,
            "state": a.state,
            "state_code": a.state_code,
            "pincode": a.pincode,
            "country": a.country,
            "is_default": a.is_default,
        } for a in party.addresses],
        bank_accounts=[{
            "id": b.id,
            "account_holder_name": b.account_holder_name,
            "bank_name": b.bank_name,
            "branch_name": b.branch_name,
            "account_number": b.account_number,
            "ifsc": b.ifsc,
            "upi_id": b.upi_id,
            "is_primary": b.is_primary,
        } for b in party.bank_accounts],
    )
```

```python
// File: backend/app/api/v1/quotations.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.quotation import (
    QuotationCreate, QuotationResponse, QuotationListResponse, QuotationAcceptRequest
)
from app.services.quotation_service import QuotationService

router = APIRouter(prefix="/quotations", tags=["Quotations"])

@router.post("/", response_model=ApiResponse[QuotationResponse])
def create_quotation(request: QuotationCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.create_quotation(db, str(company.id), request.model_dump(), None)
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.get("/", response_model=ApiResponse[QuotationListResponse])
def list_quotations(quotation_type: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    quotations = QuotationService.list_quotations(db, str(company.id), quotation_type)
    return ApiResponse(success=True, data=QuotationListResponse(
        items=[_quotation_to_response(q) for q in quotations],
        total=len(quotations)
    ))

@router.get("/{quotation_id}", response_model=ApiResponse[QuotationResponse])
def get_quotation(quotation_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.get_quotation(db, str(company.id), quotation_id)
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.post("/{quotation_id}/approve", response_model=ApiResponse[QuotationResponse])
def approve_quotation(quotation_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.approve_quotation(db, str(company.id), quotation_id)
    return ApiResponse(success=True, data=_quotation_to_response(q))

@router.post("/{quotation_id}/accept", response_model=ApiResponse[QuotationResponse])
def accept_quotation(quotation_id: str, request: QuotationAcceptRequest, company = Depends(get_current_company), db: Session = Depends(get_db)):
    q = QuotationService.accept_quotation(db, str(company.id), quotation_id, None, request.acceptance_method)
    return ApiResponse(success=True, data=_quotation_to_response(q))

def _quotation_to_response(q) -> QuotationResponse:
    lines = []
    for l in q.lines:
        lines.append({
            "id": l.id,
            "item_id": l.item_id,
            "item_name_snapshot": l.item_name_snapshot,
            "description": l.description,
            "hsn_sac_snapshot": l.hsn_sac_snapshot,
            "sku_snapshot": l.sku_snapshot,
            "quantity": float(l.quantity),
            "converted_quantity": float(l.converted_quantity),
            "unit_id": l.unit_id,
            "unit_snapshot": l.unit_snapshot,
            "rate": float(l.rate),
            "discount_type": l.discount_type,
            "discount_value": float(l.discount_value),
            "discount_amount": float(l.discount_amount),
            "tax_treatment": l.tax_treatment,
            "gst_rate": float(l.gst_rate),
            "taxable_value": float(l.taxable_value),
            "cgst_amount": float(l.cgst_amount),
            "sgst_amount": float(l.sgst_amount),
            "igst_amount": float(l.igst_amount),
            "cess_amount": float(l.cess_amount),
            "line_total": float(l.line_total)
        })
        
    return QuotationResponse(
        id=q.id,
        quotation_number=q.quotation_number,
        quotation_type=q.quotation_type.value,
        tax_treatment=q.tax_treatment,
        party_id=q.party_id,
        quotation_date=q.quotation_date,
        valid_until=q.valid_until,
        status=q.status.value,
        revision=q.revision,
        place_of_supply=q.place_of_supply,
        subtotal=float(q.subtotal),
        discount_total=float(q.discount_total),
        taxable_total=float(q.taxable_total),
        cgst_total=float(q.cgst_total),
        sgst_total=float(q.sgst_total),
        igst_total=float(q.igst_total),
        cess_total=float(q.cess_total),
        round_off=float(q.round_off),
        grand_total=float(q.grand_total),
        notes=q.notes,
        terms=q.terms,
        accepted_at=q.accepted_at,
        accepted_by=q.accepted_by,
        acceptance_method=q.acceptance_method,
        fully_converted=q.fully_converted,
        created_at=q.created_at,
        lines=lines
    )
```

```python
// File: backend/app/api/v1/returns.py
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
```

```python
// File: backend/app/api/v1/units.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.unit import UnitCreate, UnitUpdate, UnitResponse, UnitListResponse, UnitCategoryResponse
from app.services.unit_service import UnitService

router = APIRouter(prefix="/units", tags=["Units"])

@router.post("/", response_model=ApiResponse[UnitResponse])
def create_unit(request: UnitCreate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    unit = UnitService.create_unit(db, str(company.id), request.model_dump())
    return ApiResponse(success=True, data=UnitResponse(
        id=unit.id,
        company_id=unit.company_id,
        unit_name=unit.unit_name,
        symbol=unit.symbol,
        internal_code=unit.internal_code,
        gst_unit_code=unit.gst_unit_code,
        unit_type=unit.unit_type,
        base_unit_id=unit.base_unit_id,
        conversion_factor=float(unit.conversion_factor) if unit.conversion_factor else None,
        conversion_formula=unit.conversion_formula,
        precision=unit.precision,
        is_predefined=unit.is_predefined,
        is_active=unit.is_active,
        created_at=unit.created_at,
    ))

@router.get("/", response_model=ApiResponse[UnitListResponse])
def list_units(search: str = Query(None), company = Depends(get_current_company), db: Session = Depends(get_db)):
    units = UnitService.list_units(db, str(company.id), search)
    items = [UnitResponse(
        id=u.id,
        company_id=u.company_id,
        unit_name=u.unit_name,
        symbol=u.symbol,
        internal_code=u.internal_code,
        gst_unit_code=u.gst_unit_code,
        unit_type=u.unit_type,
        base_unit_id=u.base_unit_id,
        conversion_factor=float(u.conversion_factor) if u.conversion_factor else None,
        conversion_formula=u.conversion_formula,
        precision=u.precision,
        is_predefined=u.is_predefined,
        is_active=u.is_active,
        created_at=u.created_at,
    ) for u in units]
    return ApiResponse(success=True, data=UnitListResponse(items=items))

@router.get("/categories", response_model=ApiResponse[list[UnitCategoryResponse]])
def list_categories(db: Session = Depends(get_db)):
    cats = UnitService.list_categories(db)
    return ApiResponse(success=True, data=[UnitCategoryResponse(
        id=c.id, name=c.name, code=c.code, dimension=c.dimension, status=c.status
    ) for c in cats])

@router.put("/{unit_id}", response_model=ApiResponse[UnitResponse])
def update_unit(unit_id: str, request: UnitUpdate, company = Depends(get_current_company), db: Session = Depends(get_db)):
    unit = UnitService.update_unit(db, str(company.id), unit_id, request.model_dump(exclude_unset=True))
    return ApiResponse(success=True, data=UnitResponse(
        id=unit.id,
        company_id=unit.company_id,
        unit_name=unit.unit_name,
        symbol=unit.symbol,
        internal_code=unit.internal_code,
        gst_unit_code=unit.gst_unit_code,
        unit_type=unit.unit_type,
        base_unit_id=unit.base_unit_id,
        conversion_factor=float(unit.conversion_factor) if unit.conversion_factor else None,
        conversion_formula=unit.conversion_formula,
        precision=unit.precision,
        is_predefined=unit.is_predefined,
        is_active=unit.is_active,
        created_at=unit.created_at,
    ))

@router.delete("/{unit_id}", response_model=ApiResponse[dict])
def delete_unit(unit_id: str, company = Depends(get_current_company), db: Session = Depends(get_db)):
    UnitService.delete_unit(db, str(company.id), unit_id)
    return ApiResponse(success=True, data={"message": "Unit deactivated"})
```

```python
// File: backend/app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    app_env: str = "development"
    database_url: str = "sqlite:///data/gst_billing.db"
    secret_key: str = "dev-secret-key-change-in-production"
    session_secret: str = "dev-session-secret-change-in-production"
    storage_path: str = "storage"
    log_level: str = "INFO"
    cors_origins: str = "http://localhost:5173,http://localhost:3000,http://localhost:4173"
    
    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]
    
    @property
    def db_path(self) -> Path:
        return Path(self.database_url.replace("sqlite:///", ""))
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

```python
// File: backend/app/core/database.py
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=settings.app_env == "development",
)

# Enable foreign keys and WAL for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA busy_timeout=5000")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
// File: backend/app/core/exceptions.py
class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Not found"):
        super().__init__("NOT_FOUND", message, 404)

class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", fields: dict = None):
        super().__init__("VALIDATION_ERROR", message, 422)
        self.fields = fields or {}

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__("CONFLICT", message, 409)

class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__("PERMISSION_DENIED", message, 403)

class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__("AUTHENTICATION_REQUIRED", message, 401)

class InvoiceLockedException(AppException):
    def __init__(self, message: str = "Invoice is finalized and cannot be edited"):
        super().__init__("INVOICE_LOCKED", message, 409)
```

```python
// File: backend/app/core/gst/__init__.py
"""GST / Business Identity Module."""
from .validator import GSTINValidator
from .parser import GSTINParser
from .state_codes import GSTStateMaster
from .service import GSTService

__all__ = ["GSTINValidator", "GSTINParser", "GSTStateMaster", "GSTService"]
```

```python
// File: backend/app/core/gst/constants.py
GSTIN_REGEX = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
GSTN_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_LENGTH = 15
PAN_TYPES = ["C", "P", "H", "F", "A", "T", "B", "L", "J", "G"]
BANK_ACCOUNT_TYPES = {
    "SAVINGS": "Savings Account",
    "CURRENT": "Current Account",
    "CASH_CREDIT": "Cash Credit Account",
    "OVERDRAFT": "Overdraft Account",
    "NRE": "NRE Account",
    "NRO": "NRO Account",
    "OTHER": "Other",
}
```

```python
// File: backend/app/core/gst/exceptions.py
class GSTINValidationError(Exception):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InvalidGSTINLength(GSTINValidationError):
    def __init__(self, message: str = "GSTIN must be exactly 15 characters long"):
        super().__init__(message, "INVALID_LENGTH")

class InvalidGSTINFormat(GSTINValidationError):
    def __init__(self, message: str = "Invalid GSTIN format"):
        super().__init__(message, "INVALID_FORMAT")

class InvalidGSTINChecksum(GSTINValidationError):
    def __init__(self, message: str = "Invalid GSTIN checksum"):
        super().__init__(message, "INVALID_CHECKSUM")

class InvalidGSTStateCode(GSTINValidationError):
    def __init__(self, message: str = "Invalid GST state code"):
        super().__init__(message, "INVALID_STATE_CODE")
```

```python
// File: backend/app/core/gst/parser.py
from .state_codes import GSTStateMaster

class GSTINParser:
    @staticmethod
    def parse(gstin: str) -> dict:
        normalized = gstin.strip().upper()
        state_code = normalized[:2] if len(normalized) >= 2 else ""
        state_info = GSTStateMaster.get_state(state_code)
        
        return {
            "raw": gstin,
            "normalized": normalized,
            "state_code": state_code,
            "state": state_info["name"] if state_info else None,
            "is_union_territory": state_info["is_union_territory"] if state_info else False,
            "pan": normalized[2:12] if len(normalized) >= 12 else "",
            "pan_holder_type": normalized[11] if len(normalized) >= 12 else "",
            "entity_number": normalized[12] if len(normalized) >= 13 else "",
            "default_character": normalized[13] if len(normalized) >= 14 else "",
            "check_digit": normalized[14] if len(normalized) == 15 else "",
        }

    @staticmethod
    def extract_state_code(gstin: str) -> str:
        return gstin.strip().upper()[:2]

    @staticmethod
    def extract_state(gstin: str) -> str | None:
        return GSTStateMaster.get_state_name(GSTINParser.extract_state_code(gstin))

    @staticmethod
    def extract_pan(gstin: str) -> str:
        return gstin.strip().upper()[2:12]

    @staticmethod
    def extract_entity_number(gstin: str) -> str:
        return gstin.strip().upper()[12:13]
```

```python
// File: backend/app/core/gst/schemas.py
from pydantic import BaseModel
from typing import Optional

class GSTINParseResult(BaseModel):
    gstin: str
    state_code: str
    state: Optional[str]
    is_union_territory: bool
    pan: str
    pan_holder_type: str
    entity_number: str
    default_character: str
    check_digit: str

class GSTINValidationResult(BaseModel):
    gstin: str
    valid: bool
    valid_length: bool
    valid_structure: bool
    valid_state_code: bool
    valid_checksum: bool
    errors: list[str]
    parsed: Optional[GSTINParseResult] = None
    level: str

class GSTStateResponse(BaseModel):
    code: str
    name: str
    is_union_territory: bool

class PhoneNumberInput(BaseModel):
    country_code: str
    number: str
    e164: Optional[str] = None

class BankAccountType(str):
    pass
```

```python
// File: backend/app/core/gst/service.py
from .schemas import GSTINValidationResult, GSTINParseResult, GSTStateResponse
from .validator import GSTINValidator
from .parser import GSTINParser
from .state_codes import GSTStateMaster

class GSTService:
    @staticmethod
    def validate(gstin: str) -> GSTINValidationResult:
        result = GSTINValidator.validate(gstin)
        parsed = None
        if result["valid_length"] and result["valid_structure"]:
            parsed_dict = GSTINParser.parse(result["gstin"])
            parsed = GSTINParseResult(
                gstin=parsed_dict["normalized"],
                state_code=parsed_dict["state_code"],
                state=parsed_dict["state"],
                is_union_territory=parsed_dict["is_union_territory"],
                pan=parsed_dict["pan"],
                pan_holder_type=parsed_dict["pan_holder_type"],
                entity_number=parsed_dict["entity_number"],
                default_character=parsed_dict["default_character"],
                check_digit=parsed_dict["check_digit"]
            )
            
        return GSTINValidationResult(
            gstin=result["gstin"],
            valid=result["valid"],
            valid_length=result["valid_length"],
            valid_structure=result["valid_structure"],
            valid_state_code=result["valid_state_code"],
            valid_checksum=result["valid_checksum"],
            errors=result["errors"],
            parsed=parsed,
            level=result["level"]
        )

    @staticmethod
    def parse(gstin: str) -> GSTINParseResult:
        parsed_dict = GSTINParser.parse(gstin)
        return GSTINParseResult(
            gstin=parsed_dict["normalized"],
            state_code=parsed_dict["state_code"],
            state=parsed_dict["state"],
            is_union_territory=parsed_dict["is_union_territory"],
            pan=parsed_dict["pan"],
            pan_holder_type=parsed_dict["pan_holder_type"],
            entity_number=parsed_dict["entity_number"],
            default_character=parsed_dict["default_character"],
            check_digit=parsed_dict["check_digit"]
        )

    @staticmethod
    def get_state(gstin: str) -> GSTStateResponse | None:
        code = GSTINParser.extract_state_code(gstin)
        state_data = GSTStateMaster.get_state(code)
        if state_data:
            return GSTStateResponse(**state_data)
        return None

    @staticmethod
    def extract_pan(gstin: str) -> str:
        return GSTINParser.extract_pan(gstin)

    @staticmethod
    def normalize(gstin: str) -> str:
        return gstin.strip().upper()
```

```python
// File: backend/app/core/gst/state_codes.py
GST_STATE_CODES = {
    "01": ("Jammu and Kashmir", False),
    "02": ("Himachal Pradesh", False),
    "03": ("Punjab", False),
    "04": ("Chandigarh", True),
    "05": ("Uttarakhand", False),
    "06": ("Haryana", False),
    "07": ("Delhi", True),
    "08": ("Rajasthan", False),
    "09": ("Uttar Pradesh", False),
    "10": ("Bihar", False),
    "11": ("Sikkim", False),
    "12": ("Arunachal Pradesh", False),
    "13": ("Nagaland", False),
    "14": ("Manipur", False),
    "15": ("Mizoram", False),
    "16": ("Tripura", False),
    "17": ("Meghalaya", False),
    "18": ("Assam", False),
    "19": ("West Bengal", False),
    "20": ("Jharkhand", False),
    "21": ("Odisha", False),
    "22": ("Chhattisgarh", False),
    "23": ("Madhya Pradesh", False),
    "24": ("Gujarat", False),
    "25": ("Daman and Diu", True),
    "26": ("Dadra and Nagar Haveli and Daman and Diu", True),
    "27": ("Maharashtra", False),
    "29": ("Karnataka", False),
    "30": ("Goa", False),
    "31": ("Lakshadweep", True),
    "32": ("Kerala", False),
    "33": ("Tamil Nadu", False),
    "34": ("Puducherry", True),
    "35": ("Andaman and Nicobar Islands", True),
    "36": ("Telangana", False),
    "37": ("Andhra Pradesh", False),
    "38": ("Ladakh", True),
    "97": ("Other Territory", True),
    "99": ("Centre Jurisdiction", True),
}

class GSTStateMaster:
    @staticmethod
    def get_state(code: str) -> dict | None:
        state_data = GST_STATE_CODES.get(code)
        if not state_data:
            return None
        return {
            "code": code,
            "name": state_data[0],
            "is_union_territory": state_data[1]
        }

    @staticmethod
    def get_state_name(code: str) -> str | None:
        state_data = GST_STATE_CODES.get(code)
        return state_data[0] if state_data else None

    @staticmethod
    def is_valid_state_code(code: str) -> bool:
        return code in GST_STATE_CODES

    @staticmethod
    def all_states() -> list[dict]:
        return [
            {
                "code": code,
                "name": data[0],
                "is_union_territory": data[1]
            }
            for code, data in sorted(GST_STATE_CODES.items())
        ]

    @staticmethod
    def get_by_name(name: str) -> dict | None:
        name_lower = name.lower()
        for code, data in GST_STATE_CODES.items():
            if data[0].lower() == name_lower:
                return {
                    "code": code,
                    "name": data[0],
                    "is_union_territory": data[1]
                }
        return None
```

```python
// File: backend/app/core/gst/validator.py
import re
from .constants import GSTIN_REGEX, GSTN_CHARSET, GSTIN_LENGTH
from .state_codes import GSTStateMaster
from .parser import GSTINParser

class GSTINValidator:
    @staticmethod
    def validate_length(gstin: str) -> bool:
        return len(gstin.strip()) == GSTIN_LENGTH

    @staticmethod
    def validate_structure(gstin: str) -> bool:
        return bool(re.match(GSTIN_REGEX, gstin.strip().upper()))

    @staticmethod
    def validate_state_code(gstin: str) -> bool:
        code = GSTINParser.extract_state_code(gstin)
        return GSTStateMaster.is_valid_state_code(code)

    @staticmethod
    def validate_checksum(gstin: str) -> bool:
        gstin = gstin.strip().upper()
        if len(gstin) != 15:
            return False
        
        factor = 1
        sum_val = 0
        for i in range(14):
            char = gstin[i]
            if char not in GSTN_CHARSET:
                return False
            
            val = GSTN_CHARSET.index(char)
            val = val * factor
            factor = 2 if factor == 1 else 1
            
            val = (val // 36) + (val % 36)
            sum_val += val
            
        rem = sum_val % 36
        check_digit = GSTN_CHARSET[(36 - rem) % 36]
        
        return gstin[14] == check_digit

    @staticmethod
    def validate(gstin: str) -> dict:
        normalized = gstin.strip().upper()
        valid_len = GSTINValidator.validate_length(normalized)
        valid_struct = GSTINValidator.validate_structure(normalized)
        valid_state = GSTINValidator.validate_state_code(normalized)
        valid_check = GSTINValidator.validate_checksum(normalized)
        
        errors = []
        if not valid_len:
            errors.append("Invalid length")
        if not valid_struct:
            errors.append("Invalid structure")
        if not valid_state:
            errors.append("Invalid state code")
        if valid_len and valid_struct and not valid_check:
            errors.append("Invalid checksum")
            
        valid = valid_len and valid_struct and valid_state and valid_check
        
        if valid:
            level = "VALID"
        elif valid_struct and valid_state:
            level = "STRUCTURAL"
        else:
            level = "INVALID"
            
        return {
            "gstin": normalized,
            "valid": valid,
            "valid_length": valid_len,
            "valid_structure": valid_struct,
            "valid_state_code": valid_state,
            "valid_checksum": valid_check,
            "errors": errors,
            "level": level
        }
```

```python
// File: backend/app/core/security.py
import secrets
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from jose import jwt, JWTError
from app.core.config import settings

ph = PasswordHasher(time_cost=2, memory_cost=65536, parallelism=1, hash_len=32, salt_len=16)

def hash_pin(pin: str) -> str:
    return ph.hash(pin)

def verify_pin(pin: str, pin_hash: str) -> bool:
    try:
        ph.verify(pin_hash, pin)
        return True
    except VerifyMismatchError:
        return False

def create_session_token(company_id: str, session_id: str) -> str:
    payload = {
        "company_id": company_id,
        "session_id": session_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.session_secret, algorithm="HS256")

def decode_session_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.session_secret, algorithms=["HS256"])
    except JWTError:
        return None

def generate_id() -> str:
    return secrets.token_urlsafe(16)

def generate_invoice_number(series_prefix: str, current_number: int) -> str:
    return f"{series_prefix}{current_number:06d}"
```

```python
// File: backend/app/dependencies/auth.py
from fastapi import Request, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_session_token
from app.core.exceptions import AuthenticationException
from app.models.company import CompanySession, Company

async def get_current_company(request: Request, db: Session = Depends(get_db)) -> Company:
    auth_header = request.headers.get("authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationException("Missing or invalid authorization header")
    
    token = auth_header.replace("Bearer ", "")
    payload = decode_session_token(token)
    if not payload:
        raise AuthenticationException("Invalid or expired session")
    
    session = db.query(CompanySession).filter(
        CompanySession.id == payload.get("session_id"),
        CompanySession.status == "ACTIVE"
    ).first()
    
    if not session:
        raise AuthenticationException("Session not found or revoked")
    
    company = db.query(Company).filter(Company.id == payload.get("company_id")).first()
    if not company:
        raise AuthenticationException("Company not found")
    
    return company
```

```python
// File: backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.database import engine, Base
from app.core.exceptions import AppException
from app.api.v1 import api_router
from app.seed_data import seed_all
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

# Create tables
Base.metadata.create_all(bind=engine)

# Seed data
seed_all()

app = FastAPI(
    title="GST Billing API",
    version="1.0.0",
    description="GST Billing Web Application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": {"code": exc.code, "message": exc.message, "fields": getattr(exc, "fields", None)}}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"success": False, "error": {"code": "VALIDATION_ERROR", "message": "Validation error", "fields": exc.errors()}}
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": {"code": "DATABASE_ERROR", "message": "A database error occurred."}}
    )

app.include_router(api_router, prefix="/api")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={"success": False, "error": {"code": "NOT_FOUND", "message": "Endpoint not found"}}
    )

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

```python
// File: backend/app/models/__init__.py
from app.core.database import Base
from app.models.company import (
    Company, CompanyGSTDetail, CompanyAddress, CompanyContact,
    CompanyBankAccount, CompanyAsset, CompanyAuth, CompanySession
)
from app.models.unit import Unit, UnitAlias, UnitVersion
from app.models.item import Item, ItemVersion
from app.models.party import Party, PartyAddress, PartyBankAccount, PartyLedgerEntry, PaymentAllocation
from app.models.invoice import (
    Invoice, InvoiceLine, InvoiceSeries, Payment
)
from app.models.adjustment import AdjustmentNote, AdjustmentNoteLine, NoteAllocation
from app.models.order import SupplyOrder, SupplyOrderLine
from app.models.return_order import ReturnOrder, ReturnOrderLine, ReturnSettlement
from app.models.quotation import Quotation, QuotationLine, QuotationStatus, QuotationType
from app.models.boq import BOQ, BOQLine, BOQStatus, BOQItemType
from app.models.document_link import DocumentLink, DocumentLineLink
from app.models.estimate import Estimate, EstimateLine, EstimateStatus
from app.models.audit import AuditLog
from app.models.master import GSTStateCode, GSTRate, HSNSACCode

__all__ = [
    "Base",
    "Company", "CompanyGSTDetail", "CompanyAddress", "CompanyContact",
    "CompanyBankAccount", "CompanyAsset", "CompanyAuth", "CompanySession",
    "Unit", "UnitAlias", "UnitVersion",
    "Item", "ItemVersion",
    "Party", "PartyAddress", "PartyBankAccount", "PartyLedgerEntry", "PaymentAllocation",
    "Invoice", "InvoiceLine", "InvoiceSeries", "Payment", 
    "AdjustmentNote", "AdjustmentNoteLine", "NoteAllocation",
    "SupplyOrder", "SupplyOrderLine",
    "ReturnOrder", "ReturnOrderLine", "ReturnSettlement",
    "Quotation", "QuotationLine", "QuotationStatus", "QuotationType",
    "BOQ",
    "BOQLine",
    "BOQStatus",
    "BOQItemType",
    "DocumentLink",
    "DocumentLineLink",
    "Estimate", "EstimateLine", "EstimateStatus",
    "AuditLog",
    "GSTStateCode", "GSTRate", "HSNSACCode",
]
```

```python
// File: backend/app/models/adjustment.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class AdjustmentNote(Base):
    __tablename__ = "adjustment_notes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    note_number = Column(String(50), nullable=False)
    note_type = Column(String(20), nullable=False) # CREDIT_NOTE, DEBIT_NOTE
    
    source_type = Column(String(50), nullable=True)
    source_id = Column(String(36), nullable=True)
    source_number = Column(String(50), nullable=True)
    
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=True)
    invoice_number_snapshot = Column(String(50), nullable=True)
    
    original_invoice_id = Column(String(36), nullable=True)
    original_invoice_number = Column(String(100), nullable=True)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    party_role = Column(String(20), nullable=False) # CUSTOMER, SUPPLIER
    
    note_date = Column(DateTime, nullable=False)
    reason_code = Column(String(50), nullable=False)
    reason_description = Column(String(200), nullable=True)
    
    tax_treatment = Column(String(20), nullable=False) # GST, WITHOUT_GST
    gst_document = Column(Boolean, default=True)
    is_accounting_only = Column(Boolean, default=False)
    
    place_of_supply = Column(String(100), nullable=True)
    reverse_charge = Column(Boolean, default=False)
    
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    
    status = Column(String(20), default="DRAFT") # DRAFT, APPROVED, POSTED, CANCELLED, REJECTED
    
    created_by = Column(String(36), nullable=True)
    approved_by = Column(String(36), nullable=True)
    posted_by = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    posted_at = Column(DateTime, nullable=True)
    
    lines = relationship("AdjustmentNoteLine", back_populates="adjustment_note", cascade="all, delete-orphan")
    allocations = relationship("NoteAllocation", back_populates="adjustment_note", cascade="all, delete-orphan")


class AdjustmentNoteLine(Base):
    __tablename__ = "adjustment_note_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    adjustment_note_id = Column(String(36), ForeignKey("adjustment_notes.id"), nullable=False)
    
    source_line_id = Column(String(36), nullable=True)
    item_id = Column(String(36), nullable=True)
    
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    description = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    rate = Column(Numeric(15, 4), nullable=False)
    
    discount_type = Column(String(20), nullable=True)
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(String(20), nullable=True)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), default=0)
    
    adjustment_note = relationship("AdjustmentNote", back_populates="lines")


class NoteAllocation(Base):
    __tablename__ = "note_allocations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    note_id = Column(String(36), ForeignKey("adjustment_notes.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False)
    
    allocated_amount = Column(Numeric(15, 2), nullable=False)
    allocation_date = Column(DateTime, nullable=False)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)

    adjustment_note = relationship("AdjustmentNote", back_populates="allocations")
```

```python
// File: backend/app/models/audit.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    actor_id = Column(String(36), nullable=True)
    entity_type = Column(String(50), nullable=False)  # COMPANY, UNIT, ITEM, INVOICE, etc.
    entity_id = Column(String(36), nullable=False)
    action = Column(String(50), nullable=False)  # CREATED, UPDATED, DEACTIVATED, FINALIZED, etc.
    field_name = Column(String(100), nullable=True)
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    reason = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    company = relationship("Company", back_populates="audit_logs")
```

```python
// File: backend/app/models/boq.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class BOQStatus(enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    PRICED = "PRICED"
    FINALIZED = "FINALIZED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"

class BOQItemType(enum.Enum):
    MATERIAL = "MATERIAL"
    LABOUR = "LABOUR"
    SERVICE = "SERVICE"
    EQUIPMENT = "EQUIPMENT"
    SUBCONTRACT = "SUBCONTRACT"
    OTHER = "OTHER"

class BOQ(Base):
    __tablename__ = "boqs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    boq_number = Column(String(50), nullable=True)
    project_name = Column(String(200), nullable=True)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    
    boq_date = Column(DateTime, nullable=False, default=utc_now)
    version = Column(Integer, default=1)
    status = Column(Enum(BOQStatus), default=BOQStatus.DRAFT)
    
    notes = Column(Text, nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("BOQLine", back_populates="boq", cascade="all, delete-orphan")

class BOQLine(Base):
    __tablename__ = "boq_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    boq_id = Column(String(36), ForeignKey("boqs.id"), nullable=False)
    
    parent_line_id = Column(String(36), ForeignKey("boq_lines.id"), nullable=True)
    
    section = Column(String(100), nullable=True)
    item_type = Column(Enum(BOQItemType), default=BOQItemType.MATERIAL)
    
    item_id = Column(String(36), nullable=True)
    description = Column(String(255), nullable=False)
    specification = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    quantity_formula = Column(String(255), nullable=True)
    
    estimated_rate = Column(Numeric(15, 4), default=0)
    estimated_amount = Column(Numeric(15, 2), default=0)
    
    remarks = Column(Text, nullable=True)
    sort_order = Column(Integer, default=0)
    
    boq = relationship("BOQ", back_populates="lines")
    children = relationship("BOQLine")
```

```python
// File: backend/app/models/company.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_code = Column(String(20), unique=True, nullable=True)
    company_name = Column(String(200), nullable=False)
    legal_name = Column(String(200), nullable=True)
    trade_name = Column(String(200), nullable=True)
    ownership_type = Column(String(50), nullable=False)
    status = Column(String(20), default="SETUP_IN_PROGRESS")  # SETUP_IN_PROGRESS, ACTIVE, LOCKED, SUSPENDED, DEACTIVATED
    
    mobile_country_code = Column(String(5), default="+91", nullable=True)
    mobile = Column(String(20), nullable=False)
    mobile_e164 = Column(String(20), nullable=True)
    office_phone_country_code = Column(String(5), nullable=True)
    office_phone = Column(String(20), nullable=True)
    office_phone_e164 = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False)
    website = Column(String(300), nullable=True)
    logo_url = Column(String(500), nullable=True)
    
    authorized_person_name = Column(String(100), nullable=False)
    authorized_person_designation = Column(String(100), nullable=True)
    authorized_person_mobile = Column(String(20), nullable=True)
    authorized_person_email = Column(String(100), nullable=True)
    
    logo_asset_id = Column(String(36), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    version = Column(Integer, default=1)
    
    gst_details = relationship("CompanyGSTDetail", back_populates="company", uselist=False)
    addresses = relationship("CompanyAddress", back_populates="company")
    contacts = relationship("CompanyContact", back_populates="company")
    bank_accounts = relationship("CompanyBankAccount", back_populates="company")
    auth = relationship("CompanyAuth", back_populates="company", uselist=False)
    sessions = relationship("CompanySession", back_populates="company")
    audit_logs = relationship("AuditLog", back_populates="company")

class CompanyGSTDetail(Base):
    __tablename__ = "company_gst_details"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    gstin = Column(String(15), nullable=True)
    state_code = Column(String(2), nullable=True)
    state_name = Column(String(100), nullable=True)
    pan = Column(String(10), nullable=True)
    tan = Column(String(10), nullable=True)
    registration_number = Column(String(1), nullable=True)
    gstin_character_14 = Column(String(1), nullable=True)
    checksum = Column(String(1), nullable=True)
    gstin_validation_status = Column(String(20), default="NOT_VALIDATED")  # VALID, INVALID, NOT_VALIDATED
    external_verification_status = Column(String(20), default="NOT_VERIFIED")
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    company = relationship("Company", back_populates="gst_details")

class CompanyAddress(Base):
    __tablename__ = "company_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    address_type = Column(String(20), default="REGISTERED")  # REGISTERED, BILLING, SHIPPING, OFFICE
    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200), nullable=True)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False)
    state_code = Column(String(2), nullable=False)
    pincode = Column(String(10), nullable=False)
    country = Column(String(50), default="India")
    is_default = Column(Boolean, default=True)
    
    company = relationship("Company", back_populates="addresses")

class CompanyContact(Base):
    __tablename__ = "company_contacts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    contact_type = Column(String(20), default="PRIMARY")
    person_name = Column(String(100), nullable=True)
    designation = Column(String(100), nullable=True)
    mobile = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    
    company = relationship("Company", back_populates="contacts")

class CompanyBankAccount(Base):
    __tablename__ = "company_bank_accounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    account_holder_name = Column(String(100), nullable=False)
    account_number = Column(String(50), nullable=False)
    ifsc = Column(String(20), nullable=False)
    bank_name = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=False)
    branch_address = Column(String(200), nullable=True)
    account_type = Column(String(30), default="CURRENT")  # SAVINGS, CURRENT, CASH_CREDIT, OVERDRAFT, NRE, NRO, OTHER
    upi_id = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=True)
    status = Column(String(20), default="ACTIVE")
    
    company = relationship("Company", back_populates="bank_accounts")

class CompanyAsset(Base):
    __tablename__ = "company_assets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    asset_type = Column(String(30), nullable=False)  # COMPANY_LOGO, etc.
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(50), nullable=False)
    file_size = Column(Integer, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    original_width = Column(Integer, nullable=True)
    original_height = Column(Integer, nullable=True)
    standardized = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)

class CompanyAuth(Base):
    __tablename__ = "company_auth"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False, unique=True)
    pin_hash = Column(String(255), nullable=False)
    failed_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login_at = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    company = relationship("Company", back_populates="auth")

class CompanySession(Base):
    __tablename__ = "company_sessions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    session_token_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=utc_now)
    expires_at = Column(DateTime, nullable=False)
    last_activity_at = Column(DateTime, default=utc_now)
    revoked_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    company = relationship("Company", back_populates="sessions")
```

```python
// File: backend/app/models/document_link.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class DocumentLink(Base):
    __tablename__ = "document_links"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    source_type = Column(String(50), nullable=False)
    source_id = Column(String(36), nullable=False)
    source_number = Column(String(100), nullable=True)
    source_revision = Column(Integer, nullable=True)
    
    target_type = Column(String(50), nullable=False)
    target_id = Column(String(36), nullable=False)
    target_number = Column(String(100), nullable=True)
    target_revision = Column(Integer, nullable=True)
    
    relationship_type = Column(String(50), nullable=False)
    
    quantity = Column(Numeric(15, 5), nullable=True)
    amount = Column(Numeric(15, 2), nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)


class DocumentLineLink(Base):
    __tablename__ = "document_line_links"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    source_document_type = Column(String(50), nullable=False)
    source_document_id = Column(String(36), nullable=False)
    source_line_id = Column(String(36), nullable=False)
    
    target_document_type = Column(String(50), nullable=False)
    target_document_id = Column(String(36), nullable=False)
    target_line_id = Column(String(36), nullable=False)
    
    source_quantity = Column(Numeric(15, 5), nullable=True)
    converted_quantity = Column(Numeric(15, 5), nullable=True)
    
    source_amount = Column(Numeric(15, 2), nullable=True)
    converted_amount = Column(Numeric(15, 2), nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
```

```python
// File: backend/app/models/estimate.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class EstimateStatus(enum.Enum):
    DRAFT = "DRAFT"
    REVIEW = "REVIEW"
    APPROVED = "APPROVED"
    CANCELLED = "CANCELLED"
    CONVERTED_TO_QUOTATION = "CONVERTED_TO_QUOTATION"

class Estimate(Base):
    __tablename__ = "estimates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    estimate_number = Column(String(50), nullable=True)
    boq_id = Column(String(36), ForeignKey("boqs.id"), nullable=True)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    
    estimate_date = Column(DateTime, nullable=False, default=utc_now)
    valid_until = Column(DateTime, nullable=True)
    
    version = Column(Integer, default=1)
    status = Column(Enum(EstimateStatus), default=EstimateStatus.DRAFT)
    
    material_cost = Column(Numeric(15, 2), default=0)
    labour_cost = Column(Numeric(15, 2), default=0)
    service_cost = Column(Numeric(15, 2), default=0)
    other_cost = Column(Numeric(15, 2), default=0)
    
    total_cost = Column(Numeric(15, 2), default=0)
    markup_amount = Column(Numeric(15, 2), default=0)
    estimated_selling_value = Column(Numeric(15, 2), default=0)
    
    gst_total = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("EstimateLine", back_populates="estimate", cascade="all, delete-orphan")

class EstimateLine(Base):
    __tablename__ = "estimate_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    estimate_id = Column(String(36), ForeignKey("estimates.id"), nullable=False)
    
    item_name_snapshot = Column(String(255), nullable=False)
    item_type = Column(String(50), nullable=True) # Matches BOQItemType
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_snapshot = Column(String(50), nullable=True)
    
    cost_rate = Column(Numeric(15, 4), default=0)
    cost_amount = Column(Numeric(15, 2), default=0)
    
    markup_percent = Column(Numeric(5, 2), default=0)
    markup_amount = Column(Numeric(15, 2), default=0)
    
    selling_rate = Column(Numeric(15, 4), default=0)
    selling_amount = Column(Numeric(15, 2), default=0)
    
    estimate = relationship("Estimate", back_populates="lines")
```

```python
// File: backend/app/models/invoice.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    invoice_number = Column(String(50), nullable=False)
    invoice_series = Column(String(50), nullable=False)
    invoice_type = Column(String(30), default="TAX_INVOICE")
    invoice_date = Column(DateTime, nullable=False)
    accounting_period_id = Column(String(36), nullable=True)
    
    order_id = Column(String(36), ForeignKey("supply_orders.id"), nullable=True)
    transaction_type = Column(String(20), default="SALES") # SALES or PURCHASE
    
    # Customer snapshots (For SALES, this is the party. For PURCHASE, this is the company)
    customer_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    customer_name_snapshot = Column(String(200), nullable=False)
    customer_gstin_snapshot = Column(String(15), nullable=True)
    customer_address_snapshot = Column(Text, nullable=True)
    customer_state_snapshot = Column(String(100), nullable=True)
    customer_state_code_snapshot = Column(String(2), nullable=True)
    place_of_supply = Column(String(100), nullable=False)
    
    # Seller snapshots (For SALES, this is the company. For PURCHASE, this is the party)
    shipping_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    
    financial_year = Column(String(20), nullable=True)
    
    # Pre-invoice genealogy fields
    origin_document_type = Column(String(50), nullable=True)
    origin_document_id = Column(String(36), nullable=True)
    origin_document_number = Column(String(100), nullable=True)
    
    source_order_id = Column(String(36), nullable=True)
    source_order_number = Column(String(100), nullable=True)
    seller_id = Column(String(36), ForeignKey("parties.id"), nullable=True)
    seller_name_snapshot = Column(String(200), nullable=False)
    seller_gstin_snapshot = Column(String(15), nullable=True)
    seller_address_snapshot = Column(Text, nullable=True)
    seller_state_snapshot = Column(String(100), nullable=True)
    seller_state_code_snapshot = Column(String(2), nullable=True)
    
    currency_code = Column(String(3), default="INR")
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    other_charges = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(500), nullable=True)
    
    invoice_status = Column(String(20), default="DRAFT")  # DRAFT, FINALIZED, CANCELLED, VOID
    payment_status = Column(String(20), default="UNPAID")  # UNPAID, PARTIALLY_PAID, PAID
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    finalized_at = Column(DateTime, nullable=True)
    version = Column(Integer, default=1)
    
    lines = relationship("InvoiceLine", back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    item_id = Column(String(36), nullable=True)
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    description_snapshot = Column(Text, nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    unit_id = Column(String(36), nullable=True)
    unit_name_snapshot = Column(String(50), nullable=True)
    unit_symbol_snapshot = Column(String(20), nullable=True)
    conversion_factor = Column(Numeric(15, 5), default=1)
    base_quantity = Column(Numeric(15, 5), nullable=True)
    
    rate = Column(Numeric(15, 4), nullable=False)
    discount_type = Column(String(20), nullable=True)  # NONE, PERCENT, FIXED
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    taxable_value = Column(Numeric(15, 2), default=0)
    
    gst_rate = Column(Numeric(5, 2), default=0)
    cgst_rate = Column(Numeric(5, 2), default=0)
    sgst_rate = Column(Numeric(5, 2), default=0)
    igst_rate = Column(Numeric(5, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    line_total = Column(Numeric(15, 2), default=0)
    
    invoice = relationship("Invoice", back_populates="lines")

class InvoiceSeries(Base):
    __tablename__ = "invoice_series"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    document_type = Column(String(30), default="TAX_INVOICE")
    prefix = Column(String(50), nullable=False)
    suffix = Column(String(50), nullable=True)
    starting_number = Column(Integer, default=1)
    current_number = Column(Integer, default=1)
    fiscal_year = Column(String(20), nullable=True)
    reset_policy = Column(String(20), default="NEVER")  # NEVER, YEARLY
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=utc_now)

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=True)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    payment_mode = Column(String(30), nullable=False)  # CASH, BANK_TRANSFER, UPI, CARD, CHEQUE, NEFT, RTGS, IMPS
    reference_number = Column(String(100), nullable=True)
    bank_account_id = Column(String(36), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="COMPLETED")
    created_at = Column(DateTime, default=utc_now)
```

```python
// File: backend/app/models/item.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Item(Base):
    __tablename__ = "items"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    item_type = Column(String(20), nullable=False)  # PRODUCT, SERVICE
    item_name = Column(String(200), nullable=False)
    sku_code = Column(String(100), nullable=True)
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    hsn_sac_code = Column(String(20), nullable=True)
    gst_applicable = Column(Boolean, default=True)
    default_gst_rate_id = Column(String(36), ForeignKey("gst_rates.id"), nullable=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, INACTIVE, ARCHIVED
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    version = Column(Integer, default=1)
    
    versions = relationship("ItemVersion", back_populates="item", cascade="all, delete-orphan")

class ItemVersion(Base):
    __tablename__ = "item_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(String(36), ForeignKey("items.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    item_name = Column(String(200), nullable=True)
    unit_id = Column(String(36), nullable=True)
    sku_code = Column(String(100), nullable=True)
    hsn_sac_code = Column(String(20), nullable=True)
    gst_rate_id = Column(String(36), nullable=True)
    description = Column(Text, nullable=True)
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    item = relationship("Item", back_populates="versions")
```

```python
// File: backend/app/models/master.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Numeric, Boolean
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class GSTStateCode(Base):
    __tablename__ = "gst_state_codes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(2), unique=True, nullable=False)
    state_name = Column(String(100), nullable=False)
    union_territory = Column(Boolean, default=False)

class GSTRate(Base):
    __tablename__ = "gst_rates"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    rate = Column(Numeric(5, 2), nullable=False)
    display_name = Column(String(20), nullable=False)
    description = Column(String(200), nullable=True)
    effective_from = Column(DateTime, nullable=True)
    effective_to = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")

class HSNSACCode(Base):
    __tablename__ = "hsn_sac_codes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String(20), nullable=False)
    type = Column(String(10), nullable=False)  # HSN, SAC
    description = Column(String(500), nullable=True)
    gst_rate_id = Column(String(36), nullable=True)
    applicable_from = Column(DateTime, nullable=True)
    applicable_to = Column(DateTime, nullable=True)
    status = Column(String(20), default="ACTIVE")
```

```python
// File: backend/app/models/order.py
from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Enum, Text, Integer
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base


class OrderType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SALES = "SALES"

class TaxTreatment(str, enum.Enum):
    GST = "GST"
    WITHOUT_GST = "WITHOUT_GST"

class OrderStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"
    FULFILLED = "FULFILLED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class SupplyOrder(Base):
    __tablename__ = "supply_orders"

    id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)

    order_type = Column(Enum(OrderType), nullable=False)
    tax_treatment = Column(Enum(TaxTreatment), nullable=False)
    order_number = Column(String(50), nullable=True, index=True)
    
    order_date = Column(Date, nullable=False)
    expected_date = Column(Date, nullable=True)
    
    place_of_supply = Column(String(2), nullable=True) # State code
    
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT, nullable=False)
    revision = Column(Integer, default=1, nullable=False)

    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    other_charges = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(255), nullable=True)

    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)

    lines = relationship("SupplyOrderLine", back_populates="order", cascade="all, delete-orphan")
    party = relationship("Party")


class SupplyOrderLine(Base):
    __tablename__ = "supply_order_lines"

    id = Column(String(36), primary_key=True)
    order_id = Column(String(36), ForeignKey("supply_orders.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(String(36), ForeignKey("items.id"), nullable=True)

    # Snapshots
    item_name_snapshot = Column(String(255), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    unit_id = Column(String(36), nullable=False)
    unit_name_snapshot = Column(String(100), nullable=False)
    unit_symbol_snapshot = Column(String(20), nullable=False)
    
    quantity = Column(Numeric(15, 4), nullable=False)
    fulfilled_quantity = Column(Numeric(15, 4), default=0, nullable=False)
    
    rate = Column(Numeric(15, 2), nullable=False)
    
    discount_type = Column(String(20), default="NONE") # NONE, PERCENT, FIXED
    discount_value = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(Enum(TaxTreatment), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=True)

    order = relationship("SupplyOrder", back_populates="lines")
```

```python
// File: backend/app/models/party.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Party(Base):
    __tablename__ = "parties"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_code = Column(String(50), nullable=True)
    legal_name = Column(String(200), nullable=False)
    trade_name = Column(String(200), nullable=True)
    party_type = Column(String(50), nullable=False)  # Individual, Proprietorship, Partnership, LLP, Company, Other
    account_type = Column(String(20), nullable=False)  # CUSTOMER, SUPPLIER, BOTH
    contact_person = Column(String(100), nullable=True)
    mobile_country_code = Column(String(5), default="+91", nullable=True)
    mobile = Column(String(20), nullable=True)
    mobile_e164 = Column(String(20), nullable=True)
    alternate_mobile = Column(String(20), nullable=True)
    office_phone_country_code = Column(String(5), nullable=True)
    office_phone = Column(String(20), nullable=True)
    office_phone_e164 = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(300), nullable=True)
    gstin = Column(String(15), nullable=True)
    gst_registration_type = Column(String(30), default="Regular")  # Regular, Composition, Unregistered, SEZ
    gstin_status = Column(String(20), default="Unknown")  # Active, Cancelled, Suspended
    pan = Column(String(10), nullable=True)
    tan = Column(String(10), nullable=True)
    state = Column(String(100), nullable=True)
    state_code = Column(String(2), nullable=True)
    place_of_supply = Column(String(100), nullable=True)
    credit_limit = Column(Numeric(15, 2), nullable=True)
    credit_days = Column(Integer, nullable=True)
    payment_terms = Column(String(50), nullable=True)
    default_price_list = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    addresses = relationship("PartyAddress", back_populates="party", cascade="all, delete-orphan")
    bank_accounts = relationship("PartyBankAccount", back_populates="party", cascade="all, delete-orphan")
    ledger_entries = relationship("PartyLedgerEntry", back_populates="party")

class PartyAddress(Base):
    __tablename__ = "party_addresses"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    address_type = Column(String(20), default="BILLING")  # REGISTERED, BILLING, SHIPPING, OFFICE, WAREHOUSE, OTHER
    address_line_1 = Column(String(200), nullable=False)
    address_line_2 = Column(String(200), nullable=True)
    landmark = Column(String(100), nullable=True)
    city = Column(String(100), nullable=False)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=False)
    state_code = Column(String(2), nullable=False)
    pincode = Column(String(10), nullable=False)
    country = Column(String(50), default="India")
    is_default = Column(Boolean, default=True)
    
    party = relationship("Party", back_populates="addresses")

class PartyBankAccount(Base):
    __tablename__ = "party_bank_accounts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    account_holder_name = Column(String(100), nullable=True)
    bank_name = Column(String(100), nullable=True)
    branch_name = Column(String(100), nullable=True)
    account_number = Column(String(50), nullable=True)
    ifsc = Column(String(20), nullable=True)
    account_type = Column(String(30), default="CURRENT", nullable=True)  # SAVINGS, CURRENT, CASH_CREDIT, OVERDRAFT, NRE, NRO, OTHER
    upi_id = Column(String(100), nullable=True)
    is_primary = Column(Boolean, default=True)
    status = Column(String(20), default="ACTIVE")
    
    party = relationship("Party", back_populates="bank_accounts")

class PartyLedgerEntry(Base):
    __tablename__ = "party_ledger_entries"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    transaction_date = Column(DateTime, nullable=False)
    posting_date = Column(DateTime, default=utc_now)
    transaction_type = Column(String(50), nullable=False)  # Invoice, Receipt, Payment, Credit Note, Debit Note, Journal, Opening
    reference_type = Column(String(50), nullable=True)
    reference_id = Column(String(36), nullable=True)
    reference_number = Column(String(50), nullable=True)
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    currency = Column(String(3), default="INR")
    narration = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utc_now)
    
    party = relationship("Party", back_populates="ledger_entries")

class PaymentAllocation(Base):
    __tablename__ = "payment_allocations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    payment_id = Column(String(36), nullable=False)  # Can reference PartyLedgerEntry or Payment table
    invoice_id = Column(String(36), nullable=False)
    allocated_amount = Column(Numeric(15, 2), nullable=False)
    allocation_date = Column(DateTime, default=utc_now)
```

```python
// File: backend/app/models/quotation.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum, Boolean
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class QuotationType(enum.Enum):
    SALES = "SALES"
    PURCHASE = "PURCHASE"

class QuotationStatus(enum.Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    SENT = "SENT"
    VIEWED = "VIEWED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    WITHDRAWN = "WITHDRAWN"

class Quotation(Base):
    __tablename__ = "quotations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    quotation_number = Column(String(50), nullable=True)
    quotation_type = Column(Enum(QuotationType), nullable=False)
    tax_treatment = Column(String(20), nullable=False)
    
    quotation_date = Column(DateTime, nullable=False, default=utc_now)
    valid_until = Column(DateTime, nullable=False)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    status = Column(Enum(QuotationStatus), default=QuotationStatus.DRAFT)
    revision = Column(Integer, default=1)
    
    source_boq_id = Column(String(36), nullable=True)
    source_estimate_id = Column(String(36), nullable=True)
    
    place_of_supply = Column(String(100), nullable=False)
    
    # Financial Totals
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(500), nullable=True)
    
    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)
    
    accepted_at = Column(DateTime, nullable=True)
    accepted_by = Column(String(36), nullable=True)
    acceptance_method = Column(String(50), nullable=True)
    
    created_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    # Conversion Tracking
    converted_quantity_total = Column(Numeric(15, 5), default=0)
    fully_converted = Column(Boolean, default=False)
    
    lines = relationship("QuotationLine", back_populates="quotation", cascade="all, delete-orphan")

class QuotationLine(Base):
    __tablename__ = "quotation_lines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    quotation_id = Column(String(36), ForeignKey("quotations.id"), nullable=False)
    
    item_id = Column(String(36), nullable=True)
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    description = Column(Text, nullable=True)
    
    quantity = Column(Numeric(15, 5), nullable=False)
    converted_quantity = Column(Numeric(15, 5), default=0)
    
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    rate = Column(Numeric(15, 4), nullable=False)
    
    discount_type = Column(String(20), nullable=True)
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(String(20), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), default=0)
    
    quotation = relationship("Quotation", back_populates="lines")
```

```python
// File: backend/app/models/return_order.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class ReturnType(enum.Enum):
    SUPPLY_IN_RETURN = "SUPPLY_IN_RETURN"
    SUPPLY_OUT_RETURN = "SUPPLY_OUT_RETURN"

class ReturnStatus(enum.Enum):
    DRAFT = "DRAFT"
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class FinancialStatus(enum.Enum):
    NOT_REQUIRED = "NOT_REQUIRED"
    ADJUSTED = "ADJUSTED"
    REFUND_PENDING = "REFUND_PENDING"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    REFUNDED = "REFUNDED"
    CREDIT_CREATED = "CREDIT_CREATED"

class SettlementType(enum.Enum):
    ADJUST_RECEIVABLE = "ADJUST_RECEIVABLE"
    ADJUST_PAYABLE = "ADJUST_PAYABLE"
    CUSTOMER_REFUND = "CUSTOMER_REFUND"
    SUPPLIER_REFUND = "SUPPLIER_REFUND"
    CUSTOMER_CREDIT = "CUSTOMER_CREDIT"
    SUPPLIER_CREDIT = "SUPPLIER_CREDIT"

class ItemCondition(enum.Enum):
    GOOD = "GOOD"
    DAMAGED = "DAMAGED"
    DEFECTIVE = "DEFECTIVE"
    EXPIRED = "EXPIRED"
    REPAIR = "REPAIR"
    SCRAP = "SCRAP"
    OTHER = "OTHER"

class WarehouseAction(enum.Enum):
    RETURN_TO_STOCK = "RETURN_TO_STOCK"
    QUARANTINE = "QUARANTINE"
    REPAIR = "REPAIR"
    SCRAP = "SCRAP"
    RETURN_TO_SUPPLIER = "RETURN_TO_SUPPLIER"
    NONE = "NONE"

class ReturnOrder(Base):
    __tablename__ = "returns"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    
    return_number = Column(String(50), nullable=True)
    return_type = Column(Enum(ReturnType), nullable=False)
    
    original_order_id = Column(String(36), ForeignKey("supply_orders.id"), nullable=False)
    original_order_type = Column(String(20), nullable=False)
    
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    
    return_date = Column(DateTime, nullable=False, default=utc_now)
    
    status = Column(Enum(ReturnStatus), default=ReturnStatus.DRAFT)
    financial_status = Column(Enum(FinancialStatus), default=FinancialStatus.NOT_REQUIRED)
    
    reason = Column(Text, nullable=True)
    
    # Financial Totals
    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    other_charges = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(500), nullable=True)
    
    created_by = Column(String(36), nullable=True)
    approved_by = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    lines = relationship("ReturnOrderLine", back_populates="return_order", cascade="all, delete-orphan")
    settlements = relationship("ReturnSettlement", back_populates="return_order", cascade="all, delete-orphan")

class ReturnOrderLine(Base):
    __tablename__ = "return_lines"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    return_id = Column(String(36), ForeignKey("returns.id"), nullable=False)
    original_order_line_id = Column(String(36), ForeignKey("supply_order_lines.id"), nullable=False)
    item_id = Column(String(36), nullable=True)
    
    # Snapshots from original
    item_name_snapshot = Column(String(200), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    unit_id = Column(String(36), nullable=True)
    unit_snapshot = Column(String(50), nullable=True)
    
    # Quantities
    original_quantity = Column(Numeric(15, 5), nullable=False)
    previously_returned_quantity = Column(Numeric(15, 5), default=0)
    return_quantity = Column(Numeric(15, 5), nullable=False)
    remaining_quantity = Column(Numeric(15, 5), nullable=False)
    
    # Financials (snapshots from original)
    original_rate = Column(Numeric(15, 4), nullable=False)
    rate = Column(Numeric(15, 4), nullable=False)
    
    discount_type = Column(String(20), nullable=True)
    discount_value = Column(Numeric(15, 4), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(String(20), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), default=0)
    
    # Condition
    condition = Column(Enum(ItemCondition), default=ItemCondition.GOOD)
    warehouse_action = Column(Enum(WarehouseAction), default=WarehouseAction.RETURN_TO_STOCK)
    
    return_order = relationship("ReturnOrder", back_populates="lines")

class ReturnSettlement(Base):
    __tablename__ = "return_settlements"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    return_id = Column(String(36), ForeignKey("returns.id"), nullable=False)
    
    settlement_type = Column(Enum(SettlementType), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    
    payment_id = Column(String(36), nullable=True) # Linked to a Payment if it's a direct refund
    ledger_entry_id = Column(String(36), nullable=True)
    
    status = Column(String(20), default="COMPLETED")
    settlement_date = Column(DateTime, nullable=False, default=utc_now)
    reference_number = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=utc_now)
    
    return_order = relationship("ReturnOrder", back_populates="settlements")
```

```python
// File: backend/app/models/unit.py
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Integer, ForeignKey, Numeric, Text, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

class Unit(Base):
    __tablename__ = "units"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    unit_name = Column(String(100), nullable=False)
    symbol = Column(String(20), nullable=False)
    internal_code = Column(String(20), nullable=True)
    gst_unit_code = Column(String(20), nullable=True)
    category_id = Column(String(36), ForeignKey("unit_categories.id"), nullable=True)
    unit_type = Column(String(20), default="BASE")  # BASE, DERIVED, COMPOUND, COUNT, COMMERCIAL, CUSTOM
    base_unit_id = Column(String(36), ForeignKey("units.id"), nullable=True)
    conversion_factor = Column(Numeric(20, 10), nullable=True)
    conversion_formula = Column(String(500), nullable=True)
    precision = Column(Integer, default=2)
    rounding_mode = Column(String(20), default="HALF_UP")
    is_predefined = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)
    
    aliases = relationship("UnitAlias", back_populates="unit", cascade="all, delete-orphan")
    versions = relationship("UnitVersion", back_populates="unit", cascade="all, delete-orphan")

class UnitCategory(Base):
    __tablename__ = "unit_categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False)
    dimension = Column(String(50), nullable=True)
    status = Column(String(20), default="ACTIVE")

class UnitAlias(Base):
    __tablename__ = "unit_aliases"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    alias = Column(String(50), nullable=False)
    normalized_alias = Column(String(50), nullable=False)
    
    unit = relationship("Unit", back_populates="aliases")

class UnitVersion(Base):
    __tablename__ = "unit_versions"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    unit_id = Column(String(36), ForeignKey("units.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    conversion_formula = Column(String(500), nullable=True)
    conversion_factor = Column(Numeric(20, 10), nullable=True)
    effective_from = Column(DateTime, default=utc_now)
    effective_to = Column(DateTime, nullable=True)
    
    unit = relationship("Unit", back_populates="versions")
```

```python
// File: backend/app/schemas/adjustment.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class AdjustmentNoteLineBase(BaseModel):
    source_line_id: Optional[str] = None
    item_id: Optional[str] = None
    item_name_snapshot: str
    sku_snapshot: Optional[str] = None
    hsn_sac_snapshot: Optional[str] = None
    description: Optional[str] = None
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    rate: Decimal
    discount_type: Optional[str] = None
    discount_value: Decimal = Decimal('0')
    discount_amount: Decimal = Decimal('0')
    tax_treatment: Optional[str] = None
    gst_rate: Decimal = Decimal('0')
    taxable_value: Decimal = Decimal('0')
    cgst_amount: Decimal = Decimal('0')
    sgst_amount: Decimal = Decimal('0')
    igst_amount: Decimal = Decimal('0')
    cess_amount: Decimal = Decimal('0')
    line_total: Decimal = Decimal('0')

class AdjustmentNoteLineCreate(AdjustmentNoteLineBase):
    pass

class AdjustmentNoteLineResponse(AdjustmentNoteLineBase):
    id: str
    adjustment_note_id: str

    class Config:
        from_attributes = True

class AdjustmentNoteBase(BaseModel):
    note_type: str
    source_type: Optional[str] = None
    source_id: Optional[str] = None
    source_number: Optional[str] = None
    party_id: str
    party_role: str
    note_date: datetime
    reason_code: str
    reason_description: Optional[str] = None
    tax_treatment: str
    gst_document: bool = True
    is_accounting_only: bool = False
    place_of_supply: Optional[str] = None
    reverse_charge: bool = False
    subtotal: Decimal = Decimal('0')
    discount_total: Decimal = Decimal('0')
    taxable_total: Decimal = Decimal('0')
    cgst_total: Decimal = Decimal('0')
    sgst_total: Decimal = Decimal('0')
    igst_total: Decimal = Decimal('0')
    cess_total: Decimal = Decimal('0')
    round_off: Decimal = Decimal('0')
    grand_total: Decimal = Decimal('0')

class AdjustmentNoteCreate(AdjustmentNoteBase):
    lines: List[AdjustmentNoteLineCreate]

class AdjustmentNoteResponse(AdjustmentNoteBase):
    id: str
    company_id: str
    note_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    posted_at: Optional[datetime] = None
    lines: List[AdjustmentNoteLineResponse] = []

    class Config:
        from_attributes = True

class AdjustmentNoteListResponse(BaseModel):
    items: List[AdjustmentNoteResponse]
    total: int

class NoteAllocationBase(BaseModel):
    target_type: str
    target_id: str
    allocated_amount: Decimal
    allocation_date: datetime

class NoteAllocationCreate(NoteAllocationBase):
    pass

class NoteAllocationResponse(NoteAllocationBase):
    id: str
    note_id: str
    party_id: str
    created_at: datetime

    class Config:
        from_attributes = True
```

```python
// File: backend/app/schemas/auth.py
from pydantic import BaseModel, Field
from typing import Optional

class CompanySetupRequest(BaseModel):
    # Business
    company_name: str = Field(..., min_length=2, max_length=200)
    ownership_type: str = Field(...)
    authorized_person_name: str = Field(..., min_length=1, max_length=100)
    authorized_person_designation: Optional[str] = Field(None, max_length=100)

    # GST / Tax
    gst_registered: bool = True
    gstin: Optional[str] = Field(None, max_length=15)
    tan: Optional[str] = Field(None, max_length=10)

    # Address
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: Optional[str] = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")

    # Contact
    mobile: str = Field(..., min_length=7, max_length=20)
    mobile_country_code: str = Field(default="+91")
    mobile_e164: Optional[str] = Field(None, max_length=25)
    office_phone: Optional[str] = Field(None, max_length=20)
    office_phone_country_code: Optional[str] = Field(None, max_length=5)
    office_phone_e164: Optional[str] = Field(None, max_length=25)
    email: str = Field(..., max_length=100)
    website: Optional[str] = Field(None, max_length=300)

    # Bank — ALL OPTIONAL
    bank_account_holder_name: Optional[str] = Field(None, max_length=100)
    bank_account_number: Optional[str] = Field(None, max_length=50)
    bank_ifsc: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=100)
    bank_branch: Optional[str] = Field(None, max_length=100)
    bank_account_type: Optional[str] = Field(None, max_length=30)

    # Security
    pin: str = Field(..., min_length=4, max_length=4)
    confirm_pin: str = Field(..., min_length=4, max_length=4)

class LoginRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=4)

class LoginResponse(BaseModel):
    token: str
    company_name: str
    company_id: str

class CompanyProfileResponse(BaseModel):
    id: str
    company_name: str
    legal_name: Optional[str]
    ownership_type: str
    status: str
    mobile: str
    email: str
    authorized_person_name: str
    logo_url: Optional[str]
```

```python
// File: backend/app/schemas/boq.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.boq import BOQStatus, BOQItemType

class BOQLineCreate(BaseModel):
    parent_line_id: Optional[str] = None
    section: Optional[str] = None
    item_type: BOQItemType = BOQItemType.MATERIAL
    item_id: Optional[str] = None
    description: str
    specification: Optional[str] = None
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    quantity_formula: Optional[str] = None
    estimated_rate: Optional[Decimal] = Decimal('0')
    remarks: Optional[str] = None
    sort_order: int = 0

class BOQCreate(BaseModel):
    project_name: Optional[str] = None
    party_id: Optional[str] = None
    boq_date: datetime
    notes: Optional[str] = None
    lines: List[BOQLineCreate]

class BOQLineResponse(BaseModel):
    id: str
    parent_line_id: Optional[str]
    section: Optional[str]
    item_type: str
    item_id: Optional[str]
    description: str
    specification: Optional[str]
    quantity: float
    unit_id: Optional[str]
    unit_snapshot: Optional[str]
    quantity_formula: Optional[str]
    estimated_rate: float
    estimated_amount: float
    remarks: Optional[str]
    sort_order: int

class BOQResponse(BaseModel):
    id: str
    boq_number: Optional[str]
    project_name: Optional[str]
    party_id: Optional[str]
    boq_date: datetime
    version: int
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    lines: List[BOQLineResponse]

class BOQListResponse(BaseModel):
    items: List[BOQResponse]
    total: int
```

```python
// File: backend/app/schemas/common.py
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[dict] = None

class ErrorDetail(BaseModel):
    code: str
    message: str
    fields: Optional[dict] = None
```

```python
// File: backend/app/schemas/company.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CompanyAddressSchema(BaseModel):
    id: str
    address_type: str
    address_line_1: str
    address_line_2: Optional[str]
    city: str
    district: Optional[str]
    state: str
    state_code: str
    pincode: str
    country: str
    is_default: bool

class CompanyBankAccountSchema(BaseModel):
    id: str
    account_holder_name: str
    account_number: str
    ifsc: str
    bank_name: Optional[str]
    branch: str
    account_type: str
    is_primary: bool

class CompanyGSTDetailSchema(BaseModel):
    id: str
    gstin: Optional[str]
    state_code: Optional[str]
    state_name: Optional[str]
    pan: Optional[str]
    tan: Optional[str]
    gstin_validation_status: str

class CompanyDetailResponse(BaseModel):
    id: str
    company_name: str
    legal_name: Optional[str]
    trade_name: Optional[str]
    ownership_type: str
    status: str
    mobile_country_code: Optional[str] = "+91"
    mobile: str
    mobile_e164: Optional[str] = None
    office_phone_country_code: Optional[str] = None
    office_phone: Optional[str]
    office_phone_e164: Optional[str] = None
    email: str
    website: Optional[str] = None
    logo_url: Optional[str] = None
    authorized_person_name: str
    authorized_person_designation: Optional[str]
    gst_details: Optional[CompanyGSTDetailSchema]
    addresses: list[CompanyAddressSchema]
    bank_accounts: list[CompanyBankAccountSchema]
    created_at: datetime
    updated_at: datetime

class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    legal_name: Optional[str] = None
    trade_name: Optional[str] = None
    mobile: Optional[str] = None
    office_phone: Optional[str] = None
    email: Optional[str] = None
    authorized_person_name: Optional[str] = None
    authorized_person_designation: Optional[str] = None

class CompanyLogoResponse(BaseModel):
    logo_url: str
    asset_id: str
```

```python
// File: backend/app/schemas/estimate.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.estimate import EstimateStatus

class EstimateLineCreate(BaseModel):
    item_name_snapshot: str
    item_type: Optional[str] = None
    quantity: Decimal
    unit_snapshot: Optional[str] = None
    cost_rate: Optional[Decimal] = Decimal('0')
    markup_percent: Optional[Decimal] = Decimal('0')

class EstimateCreate(BaseModel):
    boq_id: Optional[str] = None
    party_id: Optional[str] = None
    estimate_date: datetime
    valid_until: Optional[datetime] = None
    lines: List[EstimateLineCreate]

class EstimateLineResponse(BaseModel):
    id: str
    item_name_snapshot: str
    item_type: Optional[str]
    quantity: float
    unit_snapshot: Optional[str]
    cost_rate: float
    cost_amount: float
    markup_percent: float
    markup_amount: float
    selling_rate: float
    selling_amount: float

class EstimateResponse(BaseModel):
    id: str
    estimate_number: Optional[str]
    boq_id: Optional[str]
    party_id: Optional[str]
    estimate_date: datetime
    valid_until: Optional[datetime]
    version: int
    status: str
    material_cost: float
    labour_cost: float
    service_cost: float
    other_cost: float
    total_cost: float
    markup_amount: float
    estimated_selling_value: float
    gst_total: float
    grand_total: float
    created_at: datetime
    updated_at: datetime
    lines: List[EstimateLineResponse]

class EstimateListResponse(BaseModel):
    items: List[EstimateResponse]
    total: int
```

```python
// File: backend/app/schemas/invoice.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class InvoiceLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    hsn_sac: Optional[str] = Field(None, max_length=20)
    quantity: float = Field(..., gt=0)
    unit_id: str = Field(...)
    unit_name: str = Field(...)
    unit_symbol: str = Field(...)
    rate: float = Field(..., ge=0)
    discount_type: str = Field(default="NONE")
    discount_value: float = Field(default=0, ge=0)
    gst_rate: float = Field(default=0, ge=0)

class InvoiceCreate(BaseModel):
    invoice_type: str = Field(default="TAX_INVOICE")
    invoice_date: date = Field(...)
    customer_id: str = Field(...)
    place_of_supply: str = Field(...)
    lines: list[InvoiceLineCreate] = Field(..., min_length=1)
    notes: Optional[str] = None
    terms: Optional[str] = None

class InvoiceCalculateRequest(BaseModel):
    customer_id: Optional[str] = None
    place_of_supply: str = Field(...)
    lines: list[InvoiceLineCreate] = Field(..., min_length=1)

class InvoiceCalculateResponse(BaseModel):
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    amount_in_words: Optional[str]
    lines: list[dict] # We can just return lines as dictionaries

class InvoiceLineResponse(BaseModel):
    id: str
    item_name: str
    description: Optional[str]
    hsn_sac_snapshot: Optional[str]
    quantity: float
    unit_name_snapshot: Optional[str]
    unit_symbol_snapshot: Optional[str]
    rate: float
    discount_amount: float
    taxable_value: float
    gst_rate: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    line_total: float

class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    invoice_type: str
    transaction_type: str
    invoice_date: date
    customer_name_snapshot: str
    customer_gstin_snapshot: Optional[str]
    place_of_supply: str
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    amount_in_words: Optional[str]
    invoice_status: str
    payment_status: str
    notes: Optional[str]
    lines: list[InvoiceLineResponse]
    created_at: datetime

class InvoiceListResponse(BaseModel):
    items: list[InvoiceResponse]
    total: int

class InvoiceFinalizeRequest(BaseModel):
    pass  # Optionally add specific finalization flags if needed in future

class InvoiceCancelRequest(BaseModel):
    cancel_reason: str = Field(..., min_length=5, max_length=500)
```

```python
// File: backend/app/schemas/item.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    item_type: str = Field(..., pattern="^(PRODUCT|SERVICE)$")
    item_name: str = Field(..., min_length=1, max_length=200)
    unit_id: str = Field(...)
    sku_code: Optional[str] = Field(None, max_length=100)
    hsn_sac_code: Optional[str] = Field(None, max_length=20)
    gst_applicable: bool = True
    gst_rate_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)

class ItemUpdate(BaseModel):
    item_name: Optional[str] = Field(None, min_length=1, max_length=200)
    unit_id: Optional[str] = None
    sku_code: Optional[str] = Field(None, max_length=100)
    hsn_sac_code: Optional[str] = Field(None, max_length=20)
    gst_applicable: Optional[bool] = None
    gst_rate_id: Optional[str] = None
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE|ARCHIVED)$")

class ItemResponse(BaseModel):
    id: str
    company_id: str
    item_type: str
    item_name: str
    sku_code: Optional[str]
    unit_id: str
    unit_name: Optional[str]
    unit_symbol: Optional[str]
    hsn_sac_code: Optional[str]
    gst_applicable: bool
    gst_rate_id: Optional[str]
    gst_rate: Optional[float]
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

class ItemListResponse(BaseModel):
    items: list[ItemResponse]
```

```python
// File: backend/app/schemas/order.py
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date
from decimal import Decimal
from app.models.order import OrderType, TaxTreatment, OrderStatus

class SupplyOrderLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name: str
    sku: Optional[str] = None
    hsn_sac: Optional[str] = None
    unit_id: str
    unit_name: str
    unit_symbol: str
    quantity: float
    rate: float
    discount_type: str = "NONE"
    discount_value: float = 0
    gst_rate: float = 0
    description: Optional[str] = None

class SupplyOrderCreate(BaseModel):
    order_type: OrderType
    tax_treatment: TaxTreatment
    party_id: str
    order_date: date
    expected_date: Optional[date] = None
    place_of_supply: str
    lines: List[SupplyOrderLineCreate] = Field(..., min_length=1)
    quotation_id: Optional[str] = None
    notes: Optional[str] = None
    terms: Optional[str] = None

class SupplyOrderCalculateRequest(BaseModel):
    tax_treatment: TaxTreatment
    party_id: Optional[str] = None
    place_of_supply: str
    lines: List[SupplyOrderLineCreate] = Field(..., min_length=1)

class SupplyOrderCalculateResponse(BaseModel):
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    grand_total: float
    amount_in_words: Optional[str]
    lines: List[dict]

class SupplyOrderLineResponse(BaseModel):
    id: str
    item_id: Optional[str]
    item_name_snapshot: str
    sku_snapshot: Optional[str]
    hsn_sac_snapshot: Optional[str]
    unit_id: str
    unit_name_snapshot: str
    unit_symbol_snapshot: str
    quantity: float
    fulfilled_quantity: float
    rate: float
    discount_type: str
    discount_value: float
    tax_treatment: str
    gst_rate: float
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: float
    line_total: float
    description: Optional[str]

class SupplyOrderResponse(BaseModel):
    id: str
    order_type: str
    tax_treatment: str
    order_number: Optional[str]
    order_date: date
    expected_date: Optional[date]
    party_id: str
    place_of_supply: str
    status: str
    revision: int
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    other_charges: float
    round_off: float
    grand_total: float
    amount_in_words: Optional[str]
    notes: Optional[str]
    terms: Optional[str]
    lines: List[SupplyOrderLineResponse]

class SupplyOrderListResponse(BaseModel):
    items: List[SupplyOrderResponse]
    total: int
```

```python
// File: backend/app/schemas/party.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PartyAddressCreate(BaseModel):
    address_type: str = Field(default="BILLING")
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: Optional[str] = Field(None, max_length=200)
    landmark: Optional[str] = Field(None, max_length=100)
    city: str = Field(..., min_length=1, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")
    is_default: bool = True

class PartyBankAccountCreate(BaseModel):
    account_holder_name: Optional[str] = Field(None, max_length=100)
    bank_name: Optional[str] = Field(None, max_length=100)
    branch_name: Optional[str] = Field(None, max_length=100)
    account_number: Optional[str] = Field(None, max_length=50)
    ifsc: Optional[str] = Field(None, max_length=20)
    account_type: Optional[str] = Field("CURRENT", max_length=30)
    upi_id: Optional[str] = Field(None, max_length=100)
    is_primary: bool = True

class PartyCreate(BaseModel):
    legal_name: str = Field(..., min_length=1, max_length=200)
    trade_name: Optional[str] = Field(None, max_length=200)
    party_type: str = Field(default="Proprietorship")
    account_type: str = Field(..., pattern="^(CUSTOMER|SUPPLIER|BOTH)$")
    contact_person: Optional[str] = Field(None, max_length=100)
    mobile_country_code: Optional[str] = Field(default="+91", max_length=5)
    mobile: Optional[str] = Field(None, max_length=20)
    mobile_e164: Optional[str] = Field(None, max_length=20)
    alternate_mobile: Optional[str] = Field(None, max_length=20)
    office_phone_country_code: Optional[str] = Field(None, max_length=5)
    office_phone: Optional[str] = Field(None, max_length=20)
    office_phone_e164: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    website: Optional[str] = Field(None, max_length=300)
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: str = Field(default="Regular")
    pan: Optional[str] = Field(None, max_length=10)
    tan: Optional[str] = Field(None, max_length=10)
    state: Optional[str] = Field(None, max_length=100)
    state_code: Optional[str] = Field(None, max_length=2)
    place_of_supply: Optional[str] = Field(None, max_length=100)
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    payment_terms: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    addresses: list[PartyAddressCreate] = []
    bank_accounts: list[PartyBankAccountCreate] = []

class PartyUpdate(BaseModel):
    legal_name: Optional[str] = Field(None, min_length=1, max_length=200)
    trade_name: Optional[str] = Field(None, max_length=200)
    party_type: Optional[str] = None
    account_type: Optional[str] = Field(None, pattern="^(CUSTOMER|SUPPLIER|BOTH)$")
    contact_person: Optional[str] = None
    mobile_country_code: Optional[str] = None
    mobile: Optional[str] = None
    mobile_e164: Optional[str] = None
    alternate_mobile: Optional[str] = None
    office_phone_country_code: Optional[str] = None
    office_phone: Optional[str] = None
    office_phone_e164: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: Optional[str] = None
    pan: Optional[str] = Field(None, max_length=10)
    tan: Optional[str] = Field(None, max_length=10)
    state: Optional[str] = None
    state_code: Optional[str] = None
    place_of_supply: Optional[str] = None
    credit_limit: Optional[float] = None
    credit_days: Optional[int] = None
    payment_terms: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")

class PartyResponse(BaseModel):
    id: str
    company_id: str
    party_code: Optional[str]
    legal_name: str
    trade_name: Optional[str]
    party_type: str
    account_type: str
    contact_person: Optional[str]
    mobile_country_code: Optional[str]
    mobile: Optional[str]
    mobile_e164: Optional[str]
    alternate_mobile: Optional[str]
    office_phone_country_code: Optional[str]
    office_phone: Optional[str]
    office_phone_e164: Optional[str]
    email: Optional[str]
    website: Optional[str]
    gstin: Optional[str]
    gst_registration_type: str
    pan: Optional[str]
    tan: Optional[str]
    state: Optional[str]
    state_code: Optional[str]
    place_of_supply: Optional[str]
    credit_limit: Optional[float]
    credit_days: Optional[int]
    payment_terms: Optional[str]
    notes: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    addresses: list[dict] = []
    bank_accounts: list[dict] = []

class PartyListResponse(BaseModel):
    items: list[PartyResponse]
```

```python
// File: backend/app/schemas/quotation.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.quotation import QuotationStatus, QuotationType

class QuotationLineCreate(BaseModel):
    item_id: Optional[str] = None
    item_name_snapshot: str
    description: Optional[str] = None
    hsn_sac_snapshot: Optional[str] = None
    sku_snapshot: Optional[str] = None
    
    quantity: Decimal
    unit_id: Optional[str] = None
    unit_snapshot: Optional[str] = None
    
    rate: Decimal
    discount_type: Optional[str] = None
    discount_value: Optional[Decimal] = Decimal('0')
    gst_rate: Optional[Decimal] = Decimal('0')

class QuotationCreate(BaseModel):
    quotation_type: QuotationType
    tax_treatment: str
    party_id: str
    
    valid_until: datetime
    place_of_supply: str
    
    notes: Optional[str] = None
    terms: Optional[str] = None
    
    lines: List[QuotationLineCreate]

class QuotationLineResponse(BaseModel):
    id: str
    item_id: Optional[str]
    item_name_snapshot: str
    description: Optional[str]
    hsn_sac_snapshot: Optional[str]
    sku_snapshot: Optional[str]
    
    quantity: float
    converted_quantity: float
    unit_id: Optional[str]
    unit_snapshot: Optional[str]
    
    rate: float
    discount_type: Optional[str]
    discount_value: float
    discount_amount: float
    
    tax_treatment: str
    gst_rate: float
    
    taxable_value: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    cess_amount: float
    
    line_total: float

class QuotationResponse(BaseModel):
    id: str
    quotation_number: Optional[str]
    quotation_type: str
    tax_treatment: str
    party_id: str
    
    quotation_date: datetime
    valid_until: datetime
    
    status: str
    revision: int
    
    place_of_supply: str
    
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    cess_total: float
    round_off: float
    grand_total: float
    
    notes: Optional[str]
    terms: Optional[str]
    
    accepted_at: Optional[datetime]
    accepted_by: Optional[str]
    acceptance_method: Optional[str]
    
    fully_converted: bool
    
    created_at: datetime
    
    lines: List[QuotationLineResponse]

class QuotationListResponse(BaseModel):
    items: List[QuotationResponse]
    total: int

class QuotationAcceptRequest(BaseModel):
    acceptance_method: str = "USER_ACCEPTED"
```

```python
// File: backend/app/schemas/return_order.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
from decimal import Decimal
from app.models.return_order import ReturnType, ReturnStatus, FinancialStatus, SettlementType, ItemCondition, WarehouseAction

class ReturnOrderLineCreate(BaseModel):
    original_order_line_id: str
    return_quantity: Decimal
    condition: Optional[ItemCondition] = ItemCondition.GOOD
    warehouse_action: Optional[WarehouseAction] = WarehouseAction.RETURN_TO_STOCK

class ReturnOrderCreate(BaseModel):
    original_order_id: str
    return_type: ReturnType
    reason: Optional[str] = None
    lines: List[ReturnOrderLineCreate]

class ReturnOrderLineResponse(BaseModel):
    id: str
    original_order_line_id: str
    item_id: Optional[str]
    item_name_snapshot: str
    sku_snapshot: Optional[str]
    hsn_sac_snapshot: Optional[str]
    unit_snapshot: Optional[str]
    
    original_quantity: float
    previously_returned_quantity: float
    return_quantity: float
    remaining_quantity: float
    
    rate: float
    taxable_value: float
    gst_rate: float
    cgst_amount: float
    sgst_amount: float
    igst_amount: float
    line_total: float
    
    condition: str
    warehouse_action: str

class ReturnSettlementResponse(BaseModel):
    id: str
    settlement_type: str
    amount: float
    status: str
    settlement_date: datetime
    reference_number: Optional[str]
    notes: Optional[str]

class ReturnOrderResponse(BaseModel):
    id: str
    return_number: Optional[str]
    return_type: str
    original_order_id: str
    party_id: str
    return_date: date
    
    status: str
    financial_status: str
    reason: Optional[str]
    
    subtotal: float
    discount_total: float
    taxable_total: float
    cgst_total: float
    sgst_total: float
    igst_total: float
    grand_total: float
    
    created_at: datetime
    lines: List[ReturnOrderLineResponse]
    settlements: List[ReturnSettlementResponse]

class ReturnOrderListResponse(BaseModel):
    items: List[ReturnOrderResponse]
    total: int

class ReturnableLineResponse(BaseModel):
    original_order_line_id: str
    item_name_snapshot: str
    unit_symbol_snapshot: Optional[str]
    rate: float
    gst_rate: float
    original_quantity: float
    previously_returned_quantity: float
    returnable_quantity: float

class ReturnableLinesResponse(BaseModel):
    order_id: str
    order_type: str
    tax_treatment: str
    lines: List[ReturnableLineResponse]

class ReturnSettlementCreate(BaseModel):
    settlement_type: SettlementType
    amount: Decimal
    reference_number: Optional[str] = None
    notes: Optional[str] = None
```

```python
// File: backend/app/schemas/unit.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UnitCreate(BaseModel):
    unit_name: str = Field(..., min_length=1, max_length=100)
    symbol: str = Field(..., min_length=1, max_length=20)
    internal_code: Optional[str] = Field(None, max_length=20)
    gst_unit_code: Optional[str] = Field(None, max_length=20)
    category_id: Optional[str] = None
    unit_type: str = Field(default="CUSTOM")
    base_unit_id: Optional[str] = None
    conversion_factor: Optional[float] = None
    conversion_formula: Optional[str] = Field(None, max_length=500)
    precision: int = Field(default=2, ge=0, le=8)
    rounding_mode: str = Field(default="HALF_UP")

class UnitResponse(BaseModel):
    id: str
    company_id: str
    unit_name: str
    symbol: str
    internal_code: Optional[str]
    gst_unit_code: Optional[str]
    unit_type: str
    base_unit_id: Optional[str]
    conversion_factor: Optional[float]
    conversion_formula: Optional[str]
    precision: int
    is_predefined: bool
    is_active: bool
    created_at: datetime

class UnitListResponse(BaseModel):
    items: list[UnitResponse]

class UnitUpdate(BaseModel):
    unit_name: Optional[str] = Field(None, min_length=1, max_length=100)
    symbol: Optional[str] = Field(None, min_length=1, max_length=20)
    internal_code: Optional[str] = Field(None, max_length=20)
    gst_unit_code: Optional[str] = Field(None, max_length=20)
    category_id: Optional[str] = None
    base_unit_id: Optional[str] = None
    conversion_factor: Optional[float] = None
    conversion_formula: Optional[str] = Field(None, max_length=500)
    precision: Optional[int] = Field(None, ge=0, le=8)
    rounding_mode: Optional[str] = None
    is_active: Optional[bool] = None

class UnitCategoryResponse(BaseModel):
    id: str
    name: str
    code: str
    dimension: Optional[str]
    status: str
```

```python
// File: backend/app/seed_data.py
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.master import GSTStateCode, GSTRate
from app.models.unit import UnitCategory
from decimal import Decimal

def seed_gst_states(db: Session):
    if db.query(GSTStateCode).first():
        return
    states = [
        ("01", "Jammu and Kashmir", False),
        ("02", "Himachal Pradesh", False),
        ("03", "Punjab", False),
        ("04", "Chandigarh", True),
        ("05", "Uttarakhand", False),
        ("06", "Haryana", False),
        ("07", "Delhi", True),
        ("08", "Rajasthan", False),
        ("09", "Uttar Pradesh", False),
        ("10", "Bihar", False),
        ("11", "Sikkim", False),
        ("12", "Arunachal Pradesh", False),
        ("13", "Nagaland", False),
        ("14", "Manipur", False),
        ("15", "Mizoram", False),
        ("16", "Tripura", False),
        ("17", "Meghalaya", False),
        ("18", "Assam", False),
        ("19", "West Bengal", False),
        ("20", "Jharkhand", False),
        ("21", "Odisha", False),
        ("22", "Chhattisgarh", False),
        ("23", "Madhya Pradesh", False),
        ("24", "Gujarat", False),
        ("25", "Daman and Diu", True),
        ("26", "Dadra and Nagar Haveli", True),
        ("27", "Maharashtra", False),
        ("28", "Andhra Pradesh", False),
        ("29", "Karnataka", False),
        ("30", "Goa", False),
        ("31", "Lakshadweep", True),
        ("32", "Kerala", False),
        ("33", "Tamil Nadu", False),
        ("34", "Puducherry", True),
        ("35", "Andaman and Nicobar Islands", True),
        ("36", "Telangana", False),
        ("37", "Andhra Pradesh (New)", False)
    ]
    for code, name, is_ut in states:
        db.add(GSTStateCode(code=code, state_name=name, union_territory=is_ut))
    db.commit()

def seed_gst_rates(db: Session):
    if db.query(GSTRate).first():
        return
    rates = [
        Decimal("0.00"),
        Decimal("0.25"),
        Decimal("1.50"),
        Decimal("3.00"),
        Decimal("5.00"),
        Decimal("12.00"),
        Decimal("18.00"),
        Decimal("28.00")
    ]
    for rate in rates:
        db.add(GSTRate(
            rate=rate,
            display_name=f"GST {rate}%",
            description=f"Standard GST Rate {rate}%"
        ))
    db.commit()

def seed_unit_categories(db: Session):
    if db.query(UnitCategory).first():
        return
    categories = [
        ("Quantity", "QTY", "COUNT"),
        ("Mass", "MASS", "MASS"),
        ("Length", "LEN", "LENGTH"),
        ("Area", "AREA", "AREA"),
        ("Volume", "VOL", "VOLUME"),
        ("Time", "TIME", "TIME"),
        ("Count", "CNT", "COUNT"),
        ("Commercial", "COMM", "COMMERCIAL")
    ]
    for name, code, dimension in categories:
        db.add(UnitCategory(name=name, code=code, dimension=dimension))
    db.commit()

def seed_all():
    db = SessionLocal()
    try:
        seed_gst_states(db)
        seed_gst_rates(db)
        seed_unit_categories(db)
        print("Database seeding completed.")
    except Exception as e:
        print(f"Seeding failed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_all()
```

```python
// File: backend/app/services/adjustment.py
from sqlalchemy.orm import Session
from app.models.adjustment import AdjustmentNote, AdjustmentNoteLine
from app.schemas.adjustment import AdjustmentNoteCreate
from app.models.audit import AuditLog
from typing import Optional, Tuple, List

class FinancialAdjustmentService:
    def __init__(self, db: Session):
        self.db = db
        
    def get_notes(self, company_id: str, note_type: Optional[str] = None) -> Tuple[List[AdjustmentNote], int]:
        query = self.db.query(AdjustmentNote).filter(AdjustmentNote.company_id == company_id)
        if note_type:
            query = query.filter(AdjustmentNote.note_type == note_type)
        total = query.count()
        items = query.order_by(AdjustmentNote.created_at.desc()).all()
        return items, total

    def get_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        return self.db.query(AdjustmentNote).filter(
            AdjustmentNote.id == note_id,
            AdjustmentNote.company_id == company_id
        ).first()

    def create_credit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        return self._create_note(note_in, company_id, "CREDIT_NOTE")
        
    def create_debit_note(self, note_in: AdjustmentNoteCreate, company_id: str) -> AdjustmentNote:
        return self._create_note(note_in, company_id, "DEBIT_NOTE")
        
    def _create_note(self, note_in: AdjustmentNoteCreate, company_id: str, note_type: str) -> AdjustmentNote:
        note_data = note_in.dict(exclude={"lines"})
        note = AdjustmentNote(
            **note_data,
            company_id=company_id,
            note_type=note_type,
            note_number=f"{'CN' if note_type == 'CREDIT_NOTE' else 'DN'}-TMP",
            status="DRAFT"
        )
        self.db.add(note)
        self.db.flush()
        
        for line_in in note_in.lines:
            line = AdjustmentNoteLine(**line_in.dict(), adjustment_note_id=note.id)
            self.db.add(line)
            
        self.db.commit()
        self.db.refresh(note)
        return note
        
    def post_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status in ["DRAFT", "APPROVED"]:
            note.status = "POSTED"
            # Implement Ledger Posting later
            self.db.commit()
            self.db.refresh(note)
        return note

    def approve_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status == "DRAFT":
            note.status = "APPROVED"
            self.db.commit()
            self.db.refresh(note)
        return note

    def cancel_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status in ["DRAFT", "APPROVED"]:
            note.status = "CANCELLED"
            self.db.commit()
            self.db.refresh(note)
        return note

    def reverse_note(self, note_id: str, company_id: str) -> Optional[AdjustmentNote]:
        note = self.get_note(note_id, company_id)
        if note and note.status == "POSTED":
            note.status = "REVERSED"
            # Implement Ledger Reversal later
            self.db.commit()
            self.db.refresh(note)
        return note
```

```python
// File: backend/app/services/audit_service.py
from sqlalchemy.orm import Session
from app.models.audit import AuditLog

class AuditService:
    @staticmethod
    def log(db: Session, company_id: str | None, entity_type: str, entity_id: str, 
            action: str, field_name: str = None, old_value: str = None, 
            new_value: str = None, reason: str = None, metadata: dict = None):
        log = AuditLog(
            company_id=company_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            metadata_json=metadata,
        )
        db.add(log)
        db.commit()
```

```python
// File: backend/app/services/auth_service.py
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.models.company import CompanyAuth, CompanySession
from app.core.security import verify_pin, create_session_token, generate_id
from app.core.exceptions import AuthenticationException, ValidationException
from app.core.config import settings

class AuthService:
    @staticmethod
    def authenticate(db: Session, company_id: str, pin: str) -> str:
        auth = db.query(CompanyAuth).filter(CompanyAuth.company_id == company_id).first()
        if not auth:
            raise AuthenticationException("Company not found")
        
        # Check lockout
        if auth.locked_until and auth.locked_until > datetime.now(timezone.utc):
            raise ValidationException("Account is temporarily locked due to failed attempts")
        
        if not verify_pin(pin, auth.pin_hash):
            auth.failed_attempts += 1
            if auth.failed_attempts >= 5:
                auth.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            db.commit()
            raise AuthenticationException("Incorrect PIN")
        
        # Success
        auth.failed_attempts = 0
        auth.locked_until = None
        auth.last_login_at = datetime.now(timezone.utc)
        db.commit()
        
        session_id = generate_id()
        token = create_session_token(str(company_id), session_id)
        
        session = CompanySession(
            id=session_id,
            company_id=str(company_id),
            session_token_hash=token,
            expires_at=datetime.now(timezone.utc) + timedelta(hours=12),
        )
        db.add(session)
        db.commit()
        
        return token
    
    @staticmethod
    def validate_session(db: Session, token: str) -> str | None:
        from app.core.security import decode_session_token
        payload = decode_session_token(token)
        if not payload:
            return None
        session = db.query(CompanySession).filter(
            CompanySession.id == payload.get("session_id"),
            CompanySession.status == "ACTIVE",
            CompanySession.expires_at > datetime.now(timezone.utc)
        ).first()
        if not session:
            return None
        return payload.get("company_id")

    @staticmethod
    def logout(db: Session, token: str):
        from app.core.security import decode_session_token
        payload = decode_session_token(token)
        if payload:
            session = db.query(CompanySession).filter(CompanySession.id == payload.get("session_id")).first()
            if session:
                session.status = "REVOKED"
                db.commit()
```

```python
// File: backend/app/services/boq_service.py
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
```

```python
// File: backend/app/services/company_service.py
from sqlalchemy.orm import Session
from app.models.company import Company, CompanyGSTDetail, CompanyAddress, CompanyBankAccount, CompanyAuth
from app.schemas.auth import CompanySetupRequest
from app.core.security import hash_pin, generate_id
from app.core.exceptions import ValidationException, ConflictException
from app.core.gst import GSTService

class CompanyService:
    @staticmethod
    def create_company(db: Session, data: CompanySetupRequest) -> Company:
        if data.pin != data.confirm_pin:
            raise ValidationException("PIN and confirmation PIN do not match")
        
        # Check existing
        existing = db.query(Company).first()
        if existing:
            raise ConflictException("A company account already exists. Please log in.")
        
        company = Company(
            company_name=data.company_name,
            legal_name=data.company_name,
            ownership_type=data.ownership_type,
            status="ACTIVE",
            mobile=data.mobile,
            mobile_country_code=data.mobile_country_code,
            mobile_e164=data.mobile_e164,
            office_phone=data.office_phone,
            office_phone_country_code=data.office_phone_country_code,
            office_phone_e164=data.office_phone_e164,
            email=data.email,
            website=data.website,
            authorized_person_name=data.authorized_person_name,
            authorized_person_designation=data.authorized_person_designation,
        )
        db.add(company)
        db.flush()
        
        # GST details
        gst_detail = None
        if data.gst_registered and data.gstin:
            gst_validation = GSTService.validate(data.gstin)
            if not gst_validation.valid:
                raise ValidationException("Invalid GSTIN. Please check the 15-character GST number.")
            
            parsed = GSTService.parse(data.gstin)
            
            gst_detail = CompanyGSTDetail(
                company_id=company.id,
                gstin=gst_validation.gstin,
                state_code=parsed.state_code,
                state_name=parsed.state,
                pan=parsed.pan,
                tan=data.tan,
                registration_number=parsed.entity_number,
                gstin_character_14=parsed.default_character,
                checksum=parsed.check_digit,
                gstin_validation_status="VALID",
            )
            db.add(gst_detail)
        
        # Address
        address = CompanyAddress(
            company_id=company.id,
            address_type="REGISTERED",
            address_line_1=data.address_line_1,
            address_line_2=data.address_line_2,
            city=data.city,
            district=data.district,
            state=data.state,
            state_code=data.state_code,
            pincode=data.pincode,
            country=data.country,
            is_default=True,
        )
        db.add(address)
        
        # Bank account — optional, only create if details provided
        if data.bank_account_number and data.bank_ifsc and data.bank_account_holder_name:
            bank = CompanyBankAccount(
                company_id=company.id,
                account_holder_name=data.bank_account_holder_name,
                account_number=data.bank_account_number,
                ifsc=data.bank_ifsc.upper(),
                bank_name=data.bank_name,
                branch=data.bank_branch or "",
                account_type=data.bank_account_type or "CURRENT",
                is_primary=True,
            )
            db.add(bank)
        
        # Auth
        auth = CompanyAuth(
            company_id=company.id,
            pin_hash=hash_pin(data.pin),
            failed_attempts=0,
        )
        db.add(auth)
        
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def get_company(db: Session, company_id: str) -> Company:
        return db.query(Company).filter(Company.id == company_id).first()
    
    @staticmethod
    def get_company_detail(db: Session, company_id: str):
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            return None
        return company

    @staticmethod
    def update_company(db: Session, company_id: str, data: dict) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValidationException("Company not found")
        
        for key, value in data.items():
            if hasattr(company, key) and value is not None:
                setattr(company, key, value)
                
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def update_company_logo(db: Session, company_id: str, logo_metadata: dict) -> Company:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ValidationException("Company not found")
        
        if not logo_metadata:
            company.logo_asset_id = None
            company.logo_url = None
            db.commit()
            return company

        from app.models.company import CompanyAsset
        # Store in CompanyAsset
        asset = CompanyAsset(
            company_id=company_id,
            asset_type="COMPANY_LOGO",
            file_path=logo_metadata["file_path"],
            mime_type=logo_metadata["mime_type"],
            file_size=logo_metadata["file_size"],
            width=logo_metadata.get("standardized_width"),
            height=logo_metadata.get("standardized_height"),
            original_width=logo_metadata.get("original_width"),
            original_height=logo_metadata.get("original_height"),
            standardized=True
        )
        db.add(asset)
        db.flush()
        
        # Update logo reference on company
        from app.services.file_storage_service import FileStorageService
        company.logo_asset_id = asset.id
        company.logo_url = FileStorageService.get_logo_serve_url(company_id)
        db.commit()
        db.refresh(company)
        return company
        
    @staticmethod
    def change_pin(db: Session, company_id: str, old_pin: str, new_pin: str):
        from app.core.security import verify_pin, hash_pin
        auth = db.query(CompanyAuth).filter(CompanyAuth.company_id == company_id).first()
        if not auth or not verify_pin(old_pin, auth.pin_hash):
            raise ValidationException("Incorrect current PIN")
        
        auth.pin_hash = hash_pin(new_pin)
        db.commit()
```

```python
// File: backend/app/services/estimate_service.py
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
```

```python
// File: backend/app/services/file_storage_service.py
"""Secure file storage service for logos, PDFs, and attachments.
"""
import os
import shutil
import hashlib
import mimetypes
from pathlib import Path
from datetime import datetime
from typing import BinaryIO, Tuple
from fastapi import UploadFile
from app.core.config import settings
from app.core.exceptions import ValidationException

# Allowed MIME types for uploads
ALLOWED_LOGO_TYPES = {"image/png", "image/jpeg", "image/webp"}
MAX_LOGO_SIZE = 5 * 1024 * 1024  # 5 MB

class FileStorageService:
    """Handles safe file storage outside the web root."""
    
    @staticmethod
    def _get_storage_path() -> Path:
        path = Path(settings.storage_path)
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def _safe_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal."""
        name = os.path.basename(filename)
        name = "".join(c for c in name if c.isalnum() or c in "._-")
        if not name:
            name = "file"
        return name
    
    @staticmethod
    def _validate_image(upload: UploadFile) -> Tuple[str, int]:
        """Validate uploaded image. Returns (mime_type, size)."""
        content_type = upload.content_type or ""
        if content_type not in ALLOWED_LOGO_TYPES:
            raise ValidationException(
                f"Invalid file type: {content_type}. Allowed: PNG, JPEG, WEBP"
            )
        
        # Read first chunk to verify it is actually an image
        header = upload.file.read(8192)
        upload.file.seek(0)
        
        # Basic magic number checks
        if content_type == "image/png" and not header.startswith(b"\\x89PNG"):
            raise ValidationException("File does not appear to be a valid PNG")
        if content_type == "image/jpeg" and not header.startswith(b"\\xff\\xd8"):
            raise ValidationException("File does not appear to be a valid JPEG")
        if content_type == "image/webp" and not header.startswith(b"RIFF"):
            raise ValidationException("File does not appear to be a valid WEBP")
        
        # Check size
        upload.file.seek(0, os.SEEK_END)
        size = upload.file.tell()
        upload.file.seek(0)
        if size > MAX_LOGO_SIZE:
            raise ValidationException(f"File too large. Max size: {MAX_LOGO_SIZE // 1024 // 1024}MB")
        
        return content_type, size
    
    @classmethod
    async def save_company_logo(cls, company_id: str, upload: UploadFile) -> dict:
        """Save and process company logo. Returns metadata dict."""
        from PIL import Image
        import io
        
        content_type = upload.content_type or ""
        if content_type not in ALLOWED_LOGO_TYPES:
            raise ValidationException(
                f"Invalid file type. Allowed: PNG, JPEG, WebP"
            )
        
        # Read file content
        data = await upload.read()
        if len(data) > MAX_LOGO_SIZE:
            raise ValidationException(f"File too large. Maximum: {MAX_LOGO_SIZE // 1024 // 1024}MB")
        
        # Open with Pillow
        try:
            img = Image.open(io.BytesIO(data))
            img.verify()  # Check integrity
            img = Image.open(io.BytesIO(data))  # Reopen after verify (verify closes it)
        except Exception:
            raise ValidationException("Invalid or corrupt image file")
        
        original_width, original_height = img.size
        if original_width < 100 or original_height < 100:
            raise ValidationException("Image too small. Minimum: 100x100 pixels")
        
        # Convert to RGB for WebP (handles RGBA/P mode)
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if img.mode in ("P", "LA") else "RGB")
        
        # Center crop to square
        w, h = img.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        img = img.crop((left, top, left + min_dim, top + min_dim))
        
        # Resize to standard 600x600
        TARGET_SIZE = 600
        img = img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)
        
        # Convert RGBA to RGB for WebP saving (WebP supports RGBA, but keep as RGBA for transparency)
        # Save as WebP
        storage = cls._get_storage_path()
        logo_dir = storage / "company-logos" / company_id
        logo_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = logo_dir / "company_logo.webp"
        
        # Save
        output = io.BytesIO()
        img.save(output, format="WEBP", quality=95)
        output.seek(0)
        with open(file_path, "wb") as f:
            f.write(output.getvalue())
        
        return {
            "file_path": str(file_path.relative_to(storage)),
            "mime_type": "image/webp",
            "file_size": len(output.getvalue()),
            "filename": "company_logo.webp",
            "original_width": original_width,
            "original_height": original_height,
            "standardized_width": TARGET_SIZE,
            "standardized_height": TARGET_SIZE,
        }

    @staticmethod
    def get_logo_serve_url(company_id: str) -> str | None:
        """Get the URL to serve the company logo."""
        return f"/api/v1/company/logo/{company_id}"
    
    @classmethod
    def save_invoice_pdf(cls, company_id: str, invoice_id: str, pdf_bytes: bytes) -> Path:
        """Save generated invoice PDF."""
        storage = cls._get_storage_path()
        pdf_dir = storage / "invoices" / company_id
        pdf_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = pdf_dir / f"{invoice_id}.pdf"
        with open(file_path, "wb") as f:
            f.write(pdf_bytes)
        return file_path
    
    @classmethod
    def get_file_path(cls, relative_path: str) -> Path:
        """Resolve a stored relative path to absolute path."""
        storage = cls._get_storage_path()
        target = storage / relative_path
        # Security: ensure resolved path is within storage
        try:
            target.resolve().relative_to(storage.resolve())
        except ValueError:
            raise ValidationException("Invalid file path")
        return target
```

```python
// File: backend/app/services/gst.py
from decimal import Decimal

class GSTCalculationService:
    @staticmethod
    def determine_supply_type(company_state: str, place_of_supply: str) -> str:
        return "INTRA_STATE" if company_state == place_of_supply else "INTER_STATE"
        
    @staticmethod
    def calculate_tax(taxable_value: Decimal, gst_rate: Decimal, supply_type: str) -> dict:
        tax_amount = taxable_value * (gst_rate / Decimal('100'))
        if supply_type == "INTRA_STATE":
            half_tax = tax_amount / Decimal('2')
            return {
                "cgst": half_tax,
                "sgst": half_tax,
                "igst": Decimal('0'),
                "cess": Decimal('0')
            }
        else:
            return {
                "cgst": Decimal('0'),
                "sgst": Decimal('0'),
                "igst": tax_amount,
                "cess": Decimal('0')
            }
```

```python
// File: backend/app/services/invoice_creation_service.py
from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceLine
from app.models.document_link import DocumentLink
import uuid
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class InvoiceCreationService:
    def __init__(self, db: Session):
        self.db = db
        
    def _calculate_gst(self, items):
        # Implementation to centralize GST logic
        pass

    def create_from_order(self, order_id: str, company_id: str, created_by: str) -> Invoice:
        # Fetch supply order and validate
        # Then create draft invoice with proper origin links
        # Create DocumentLink record
        # Return draft invoice
        pass

    def convert_to_final(self, invoice_id: str):
        # BEGIN TRANSACTION logic
        # Assign series number
        # Set FINALIZED
        # COMMIT
        pass
```

```python
// File: backend/app/services/invoice_number_service.py
"""Atomic invoice numbering service.
Ensures unique, sequential invoice numbers within a series.
"""
from sqlalchemy.orm import Session
from app.models.invoice import InvoiceSeries
from app.core.exceptions import ValidationException

class InvoiceNumberService:
    """Handles atomic invoice number assignment using row-level locking."""
    
    @staticmethod
    def get_or_create_series(
        db: Session,
        company_id: str,
        document_type: str = "TAX_INVOICE",
        prefix: str = "INV-",
        fiscal_year: str | None = None,
    ) -> InvoiceSeries:
        series = db.query(InvoiceSeries).filter(
            InvoiceSeries.company_id == company_id,
            InvoiceSeries.document_type == document_type,
            InvoiceSeries.prefix == prefix,
            InvoiceSeries.status == "ACTIVE",
        ).first()
        
        if not series:
            series = InvoiceSeries(
                company_id=company_id,
                document_type=document_type,
                prefix=prefix,
                starting_number=1,
                current_number=1,
                fiscal_year=fiscal_year,
            )
            db.add(series)
            db.flush()
        return series
    
    @staticmethod
    def assign_number(db: Session, series: InvoiceSeries) -> str:
        """Atomically assign next invoice number.
        
        Uses SELECT FOR UPDATE to prevent duplicate numbers under concurrency.
        """
        # Re-fetch with lock
        locked_series = db.query(InvoiceSeries).filter(
            InvoiceSeries.id == series.id
        ).with_for_update().first()
        
        if not locked_series:
            raise ValidationException("Invoice series not found")
        
        number = f"{locked_series.prefix}{locked_series.current_number:06d}"
        locked_series.current_number += 1
        return number
```

```python
// File: backend/app/services/invoice_service.py
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
        
        calculated = InvoiceService.calculate_invoice(db, company_id, company, data)
        
        # Process lines
        for line_data in calculated["lines"]:
            line = InvoiceLine(
                invoice_id=invoice.id,
                item_id=line_data.get("item_id"),
                item_name_snapshot=line_data["item_name"],
                sku_snapshot=line_data.get("sku"),
                description_snapshot=line_data.get("description"),
                hsn_sac_snapshot=line_data.get("hsn_sac_snapshot"),
                quantity=Decimal(str(line_data["quantity"])),
                unit_id=line_data.get("unit_id"),
                unit_name_snapshot=line_data.get("unit_name_snapshot"),
                unit_symbol_snapshot=line_data.get("unit_symbol_snapshot"),
                rate=Decimal(str(line_data["rate"])),
                discount_type=line_data.get("discount_type", "NONE"),
                discount_value=Decimal(str(line_data.get("discount_value", 0))),
                discount_amount=Decimal(str(line_data["discount_amount"])),
                taxable_value=Decimal(str(line_data["taxable_value"])),
                gst_rate=Decimal(str(line_data["gst_rate"])),
                cgst_rate=Decimal(str(line_data["cgst_rate"])),
                sgst_rate=Decimal(str(line_data["sgst_rate"])),
                igst_rate=Decimal(str(line_data["igst_rate"])),
                cgst_amount=Decimal(str(line_data["cgst_amount"])),
                sgst_amount=Decimal(str(line_data["sgst_amount"])),
                igst_amount=Decimal(str(line_data["igst_amount"])),
                line_total=Decimal(str(line_data["line_total"])),
            )
            db.add(line)
        
        invoice.subtotal = Decimal(str(calculated["subtotal"]))
        invoice.discount_total = Decimal(str(calculated["discount_total"]))
        invoice.taxable_total = Decimal(str(calculated["taxable_total"]))
        invoice.cgst_total = Decimal(str(calculated["cgst_total"]))
        invoice.sgst_total = Decimal(str(calculated["sgst_total"]))
        invoice.igst_total = Decimal(str(calculated["igst_total"]))
        invoice.grand_total = Decimal(str(calculated["grand_total"]))
        invoice.amount_in_words = calculated["amount_in_words"]
        
        db.commit()
        db.refresh(invoice)
        AuditService.log(db, company_id, "INVOICE", invoice.id, "CREATED")
        return invoice
    
    @staticmethod
    def calculate_invoice(db: Session, company_id: str, company, data: dict):
        # Determine interstate by checking company vs customer (if provided)
        seller_state = company.addresses[0].state_code if company.addresses else None
        customer_state = None
        if data.get("customer_id"):
            customer = db.query(Party).filter(
                Party.id == data["customer_id"],
                Party.company_id == company_id
            ).first()
            if customer:
                customer_state = customer.state_code
        
        is_interstate = (seller_state or "") != (customer_state or "")
        
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
            
            calculated_lines.append({
                "item_id": line_data.get("item_id"),
                "item_name": line_data["item_name"],
                "sku": line_data.get("sku"),
                "description": line_data.get("description"),
                "hsn_sac_snapshot": line_data.get("hsn_sac"),
                "quantity": float(qty),
                "unit_id": line_data.get("unit_id"),
                "unit_name_snapshot": line_data.get("unit_name"),
                "unit_symbol_snapshot": line_data.get("unit_symbol"),
                "rate": float(rate),
                "discount_type": discount_type,
                "discount_value": float(discount_value),
                "discount_amount": float(discount_amount),
                "taxable_value": float(taxable),
                "gst_rate": float(gst_rate),
                "cgst_rate": float(gst_rate / 2 if not is_interstate else 0),
                "sgst_rate": float(gst_rate / 2 if not is_interstate else 0),
                "igst_rate": float(gst_rate if is_interstate else 0),
                "cgst_amount": float(cgst_amount),
                "sgst_amount": float(sgst_amount),
                "igst_amount": float(igst_amount),
                "line_total": float(line_total),
            })
            
            subtotal += gross
            discount_total += discount_amount
            taxable_total += taxable
            cgst_total += cgst_amount
            sgst_total += sgst_amount
            igst_total += igst_amount
        
        grand_total = (taxable_total + cgst_total + sgst_total + igst_total).quantize(Decimal("0.01"))
        
        return {
            "subtotal": float(subtotal),
            "discount_total": float(discount_total),
            "taxable_total": float(taxable_total),
            "cgst_total": float(cgst_total),
            "sgst_total": float(sgst_total),
            "igst_total": float(igst_total),
            "grand_total": float(grand_total),
            "amount_in_words": amount_in_words(float(grand_total)),
            "lines": calculated_lines,
        }
    
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
    def list_invoices(db: Session, company_id: str, status: str = None, transaction_type: str = None) -> list[Invoice]:
        query = db.query(Invoice).filter(Invoice.company_id == company_id)
        if status:
            query = query.filter(Invoice.invoice_status == status)
        if transaction_type:
            query = query.filter(Invoice.transaction_type == transaction_type)
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
```

```python
// File: backend/app/services/item_service.py
from sqlalchemy.orm import Session
from app.models.item import Item, ItemVersion
from app.models.unit import Unit
from app.core.exceptions import ValidationException, NotFoundException, ConflictException
from app.services.audit_service import AuditService

class ItemService:
    @staticmethod
    def create_item(db: Session, company_id: str, data: dict) -> Item:
        # Check SKU uniqueness
        if data.get("sku_code"):
            existing = db.query(Item).filter(
                Item.company_id == company_id,
                Item.sku_code.ilike(data["sku_code"].strip())
            ).first()
            if existing:
                raise ConflictException("SKU code already exists for this company")
        
        item = Item(
            company_id=company_id,
            item_type=data["item_type"],
            item_name=data["item_name"].strip(),
            sku_code=data.get("sku_code"),
            unit_id=data["unit_id"],
            hsn_sac_code=data.get("hsn_sac_code"),
            gst_applicable=data.get("gst_applicable", True),
            default_gst_rate_id=data.get("gst_rate_id"),
            description=data.get("description"),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        AuditService.log(db, company_id, "ITEM", item.id, "CREATED")
        return ItemService.get_item(db, company_id, item.id)
    
    @staticmethod
    def update_item(db: Session, company_id: str, item_id: str, data: dict) -> Item:
        item = db.query(Item).filter(Item.id == item_id, Item.company_id == company_id).first()
        if not item:
            raise NotFoundException("Item not found")
        
        # Check SKU uniqueness if changing
        if data.get("sku_code") and data["sku_code"] != item.sku_code:
            existing = db.query(Item).filter(
                Item.company_id == company_id,
                Item.sku_code.ilike(data["sku_code"].strip()),
                Item.id != item_id
            ).first()
            if existing:
                raise ConflictException("SKU code already exists")
        
        # Track changes for audit
        changes = []
        for field in ["item_name", "sku_code", "unit_id", "hsn_sac_code", "gst_applicable", "default_gst_rate_id", "description", "status"]:
            if field in data and getattr(item, field) != data[field]:
                changes.append(f"{field}: {getattr(item, field)} -> {data[field]}")
                setattr(item, field, data[field])
        
        item.version += 1
        db.commit()
        db.refresh(item)
        
        if changes:
            AuditService.log(db, company_id, "ITEM", item.id, "UPDATED", reason="; ".join(changes))
        return ItemService.get_item(db, company_id, item.id)
    
    @staticmethod
    def list_items(db: Session, company_id: str, search: str = None):
        query = db.query(Item, Unit).outerjoin(Unit, Item.unit_id == Unit.id).filter(
            Item.company_id == company_id
        )
        if search:
            query = query.filter(
                Item.item_name.ilike(f"%{search}%") | 
                Item.sku_code.ilike(f"%{search}%")
            )
        results = query.order_by(Item.item_name).all()
        items = []
        for item, unit in results:
            d = {
                "id": item.id,
                "company_id": item.company_id,
                "item_type": item.item_type,
                "item_name": item.item_name,
                "sku_code": item.sku_code,
                "unit_id": item.unit_id,
                "unit_name": unit.unit_name if unit else None,
                "unit_symbol": unit.symbol if unit else None,
                "hsn_sac_code": item.hsn_sac_code,
                "gst_applicable": item.gst_applicable,
                "gst_rate_id": item.default_gst_rate_id,
                "gst_rate": None,
                "description": item.description,
                "status": item.status,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            items.append(d)
        return items
    
    @staticmethod
    def get_item(db: Session, company_id: str, item_id: str):
        from app.models.master import GSTRate
        result = db.query(Item, Unit, GSTRate).outerjoin(Unit, Item.unit_id == Unit.id).outerjoin(GSTRate, Item.default_gst_rate_id == GSTRate.id).filter(
            Item.id == item_id, Item.company_id == company_id
        ).first()
        if not result:
            raise NotFoundException("Item not found")
            
        item, unit, gst_rate = result
        return {
            "id": item.id,
            "company_id": item.company_id,
            "item_type": item.item_type,
            "item_name": item.item_name,
            "sku_code": item.sku_code,
            "unit_id": item.unit_id,
            "unit_name": unit.unit_name if unit else None,
            "unit_symbol": unit.symbol if unit else None,
            "hsn_sac_code": item.hsn_sac_code,
            "gst_applicable": item.gst_applicable,
            "gst_rate_id": item.default_gst_rate_id,
            "gst_rate": float(gst_rate.rate) if gst_rate else None,
            "description": item.description,
            "status": item.status,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    @staticmethod
    def delete_item(db: Session, company_id: str, item_id: str):
        item = db.query(Item).filter(Item.id == item_id, Item.company_id == company_id).first()
        if not item:
            raise NotFoundException("Item not found")
        
        # Check if used in invoices
        from app.models.invoice import InvoiceLine
        in_use = db.query(InvoiceLine).filter(InvoiceLine.item_id == item_id).first()
        if in_use:
            item.status = 'ARCHIVED'
            db.commit()
            AuditService.log(db, company_id, "ITEM", item.id, "ARCHIVED")
        else:
            db.delete(item)
            db.commit()
            AuditService.log(db, company_id, "ITEM", item.id, "DELETED")
```

```python
// File: backend/app/services/order_service.py
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
```

```python
// File: backend/app/services/party_service.py
from sqlalchemy.orm import Session
from app.models.party import Party, PartyAddress, PartyBankAccount
from app.core.exceptions import NotFoundException, ValidationException
from app.services.audit_service import AuditService
from app.core.gst import GSTService

class PartyService:
    @staticmethod
    def create_party(db: Session, company_id: str, data: dict) -> Party:
        if data.get("gstin"):
            gst_result = GSTService.validate(data["gstin"])
            if not gst_result.valid:
                raise ValidationException("Invalid GSTIN format")
            parsed = GSTService.parse(data["gstin"])
            data["gstin"] = gst_result.gstin
            data["pan"] = parsed.pan
            if not data.get("state_code"):
                data["state_code"] = parsed.state_code
            if not data.get("state"):
                data["state"] = parsed.state

        party = Party(
            company_id=company_id,
            legal_name=data["legal_name"],
            trade_name=data.get("trade_name"),
            party_type=data.get("party_type", "Proprietorship"),
            account_type=data["account_type"],
            contact_person=data.get("contact_person"),
            mobile_country_code=data.get("mobile_country_code"),
            mobile=data.get("mobile"),
            mobile_e164=data.get("mobile_e164"),
            alternate_mobile=data.get("alternate_mobile"),
            office_phone_country_code=data.get("office_phone_country_code"),
            office_phone=data.get("office_phone"),
            office_phone_e164=data.get("office_phone_e164"),
            email=data.get("email"),
            website=data.get("website"),
            gstin=data.get("gstin"),
            gst_registration_type=data.get("gst_registration_type", "Regular"),
            pan=data.get("pan"),
            tan=data.get("tan"),
            state=data.get("state"),
            state_code=data.get("state_code"),
            place_of_supply=data.get("place_of_supply"),
            credit_limit=data.get("credit_limit"),
            credit_days=data.get("credit_days"),
            payment_terms=data.get("payment_terms"),
            notes=data.get("notes"),
        )
        db.add(party)
        db.flush()
        
        for addr_data in data.get("addresses", []):
            addr = PartyAddress(party_id=party.id, **addr_data)
            db.add(addr)
        
        for bank_data in data.get("bank_accounts", []):
            bank = PartyBankAccount(party_id=party.id, **bank_data)
            db.add(bank)
        
        db.commit()
        db.refresh(party)
        AuditService.log(db, company_id, "PARTY", party.id, "CREATED")
        return party
    
    @staticmethod
    def update_party(db: Session, company_id: str, party_id: str, data: dict) -> Party:
        party = db.query(Party).filter(Party.id == party_id, Party.company_id == company_id).first()
        if not party:
            raise NotFoundException("Party not found")
        
        if data.get("gstin") and data.get("gstin") != party.gstin:
            gst_result = GSTService.validate(data["gstin"])
            if not gst_result.valid:
                raise ValidationException("Invalid GSTIN format")
            parsed = GSTService.parse(data["gstin"])
            data["gstin"] = gst_result.gstin
            if not data.get("pan"):
                data["pan"] = parsed.pan
            if not data.get("state_code"):
                data["state_code"] = parsed.state_code
            if not data.get("state"):
                data["state"] = parsed.state

        for field in ["legal_name", "trade_name", "party_type", "account_type", "contact_person",
                      "mobile_country_code", "mobile", "mobile_e164", "alternate_mobile",
                      "office_phone_country_code", "office_phone", "office_phone_e164",
                      "email", "website", "gstin", "gst_registration_type", "pan", "tan", "state", 
                      "state_code", "place_of_supply", "credit_limit", "credit_days", 
                      "payment_terms", "notes", "status"]:
            if field in data:
                setattr(party, field, data[field])
        
        db.commit()
        db.refresh(party)
        AuditService.log(db, company_id, "PARTY", party.id, "UPDATED")
        return party
    
    @staticmethod
    def list_parties(db: Session, company_id: str, account_type: str = None, search: str = None):
        query = db.query(Party).filter(Party.company_id == company_id)
        if account_type:
            query = query.filter(Party.account_type.in_([account_type, "BOTH"]))
        if search:
            query = query.filter(
                Party.legal_name.ilike(f"%{search}%") | 
                Party.gstin.ilike(f"%{search}%")
            )
        return query.order_by(Party.legal_name).all()
    
    @staticmethod
    def get_party(db: Session, company_id: str, party_id: str):
        party = db.query(Party).filter(Party.id == party_id, Party.company_id == company_id).first()
        if not party:
            raise NotFoundException("Party not found")
        return party
```

```python
// File: backend/app/services/pdf_service.py
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.models.invoice import Invoice

class PdfService:
    @staticmethod
    def generate_invoice_pdf(invoice: Invoice) -> bytes:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=30,
            leftMargin=30,
            topMargin=30,
            bottomMargin=30,
        )

        elements = []
        styles = getSampleStyleSheet()
        
        # Header
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=1, # Center
            spaceAfter=20
        )
        
        doc_title = "TAX INVOICE"
        if invoice.invoice_status == "DRAFT":
            doc_title = "PROFORMA INVOICE / DRAFT"
        elif invoice.invoice_status == "CANCELLED":
            doc_title = "CANCELLED INVOICE"
            
        elements.append(Paragraph(doc_title, title_style))
        
        # Company & Customer Details
        header_data = [
            [
                Paragraph(f"<b>{invoice.seller_name_snapshot}</b><br/>"
                         f"{invoice.seller_address_snapshot}<br/>"
                         f"GSTIN: {invoice.seller_gstin_snapshot or 'N/A'}<br/>"
                         f"State: {invoice.seller_state_snapshot} ({invoice.seller_state_code_snapshot})", styles['Normal']),
                Paragraph(f"<b>Billed To:</b><br/>"
                         f"<b>{invoice.customer_name_snapshot}</b><br/>"
                         f"{invoice.customer_address_snapshot or ''}<br/>"
                         f"GSTIN: {invoice.customer_gstin_snapshot or 'N/A'}<br/>"
                         f"State: {invoice.customer_state_snapshot} ({invoice.customer_state_code_snapshot})<br/>"
                         f"Place of Supply: {invoice.place_of_supply}", styles['Normal'])
            ],
            [
                Paragraph(f"<b>Invoice Number:</b> {invoice.invoice_number}<br/>"
                         f"<b>Invoice Date:</b> {invoice.invoice_date.strftime('%d-%b-%Y')}", styles['Normal']),
                ""
            ]
        ]
        
        header_table = Table(header_data, colWidths=[270, 270])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('SPAN', (0, 1), (1, 1)),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 20))
        
        # Items Table
        items_data = [
            ['S.No', 'Description', 'HSN/SAC', 'Qty', 'Unit', 'Rate', 'GST %', 'Amount']
        ]
        
        for idx, line in enumerate(invoice.lines, 1):
            items_data.append([
                str(idx),
                Paragraph(line.item_name_snapshot, styles['Normal']),
                line.hsn_sac_snapshot or '-',
                str(line.quantity.normalize()),
                line.unit_symbol_snapshot or '-',
                f"{line.rate:.2f}",
                f"{line.gst_rate}%",
                f"{line.line_total:.2f}"
            ])
            
        items_table = Table(items_data, colWidths=[30, 150, 60, 50, 40, 60, 50, 90])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            ('ALIGN', (3, 1), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
        ]))
        
        elements.append(items_table)
        
        # Totals
        totals_data = [
            ['Subtotal:', f"{invoice.subtotal:.2f}"],
            ['Discount:', f"{invoice.discount_total:.2f}"],
            ['Taxable Value:', f"{invoice.taxable_total:.2f}"],
        ]
        
        if invoice.igst_total > 0:
            totals_data.append(['IGST:', f"{invoice.igst_total:.2f}"])
        else:
            totals_data.append(['CGST:', f"{invoice.cgst_total:.2f}"])
            totals_data.append(['SGST:', f"{invoice.sgst_total:.2f}"])
            
        totals_data.append(['Grand Total:', f"{invoice.grand_total:.2f}"])
        
        totals_table = Table(totals_data, colWidths=[400, 130])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('LINEBELOW', (0, -2), (-1, -2), 0.5, colors.grey),
            ('LINEABOVE', (0, -1), (-1, -1), 0.5, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 4)
        ]))
        
        elements.append(totals_table)
        elements.append(Spacer(1, 20))
        
        # Amount in Words
        if invoice.amount_in_words:
            elements.append(Paragraph(f"<b>Amount in Words:</b> Rupees {invoice.amount_in_words}", styles['Normal']))
            
        if invoice.notes or invoice.terms:
            elements.append(Spacer(1, 20))
            if invoice.notes:
                elements.append(Paragraph(f"<b>Notes:</b><br/>{invoice.notes}", styles['Normal']))
                elements.append(Spacer(1, 10))
            if invoice.terms:
                elements.append(Paragraph(f"<b>Terms & Conditions:</b><br/>{invoice.terms}", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
```

```python
// File: backend/app/services/quotation_service.py
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.models.quotation import Quotation, QuotationLine, QuotationStatus, QuotationType
from app.models.item import Item
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
```

```python
// File: backend/app/services/return_service.py
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
```

```python
// File: backend/app/services/tax_service.py
"""GST Tax Calculation Engine.
Determines applicable tax treatment based on transaction rules.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any
from app.models.company import CompanyGSTDetail
from app.models.party import Party

class TaxService:
    """Authoritative tax calculation service.
    
    Rules applied:
    - Intra-state (seller state == place of supply): CGST + SGST/UTGST
    - Inter-state (seller state != place of supply): IGST
    - GST rate is snapshotted from item master at transaction time
    """
    
    @staticmethod
    def determine_tax_treatment(
        seller_state_code: str,
        customer_state_code: str,
        place_of_supply_state_code: str,
        customer_gstin: str | None = None,
    ) -> Dict[str, Any]:
        """Determine tax treatment for a transaction.
        
        Returns dict with:
            - is_interstate: bool
            - cgst_applicable: bool
            - sgst_applicable: bool
            - igst_applicable: bool
            - tax_split_ratio: dict (for dividing tax into components)
        """
        # Use place of supply as the determining factor for destination-based GST
        pos_code = place_of_supply_state_code or customer_state_code
        seller = seller_state_code or ""
        
        is_interstate = seller != pos_code
        
        # Unregistered customers may still attract IGST if inter-state
        # SEZ, Export, Composition etc. would extend here in future
        
        return {
            "is_interstate": is_interstate,
            "cgst_applicable": not is_interstate,
            "sgst_applicable": not is_interstate,
            "igst_applicable": is_interstate,
            "tax_split_ratio": {
                "cgst": Decimal("0.5"),
                "sgst": Decimal("0.5"),
                "igst": Decimal("1.0"),
            } if not is_interstate else {
                "cgst": Decimal("0"),
                "sgst": Decimal("0"),
                "igst": Decimal("1.0"),
            }
        }
    
    @staticmethod
    def calculate_line_tax(
        taxable_value: Decimal,
        gst_rate: Decimal,
        treatment: Dict[str, Any],
        precision: int = 2
    ) -> Dict[str, Decimal]:
        """Calculate tax components for a single line.
        
        Returns:
            {
                "cgst_rate": Decimal,
                "sgst_rate": Decimal,
                "igst_rate": Decimal,
                "cgst_amount": Decimal,
                "sgst_amount": Decimal,
                "igst_amount": Decimal,
                "total_tax": Decimal,
            }
        """
        quantize = Decimal("0.01")
        
        if treatment["is_interstate"]:
            cgst_rate = Decimal("0")
            sgst_rate = Decimal("0")
            igst_rate = gst_rate
            igst_amount = (taxable_value * igst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            cgst_amount = Decimal("0")
            sgst_amount = Decimal("0")
        else:
            half_rate = (gst_rate / 2).quantize(quantize, rounding=ROUND_HALF_UP)
            cgst_rate = half_rate
            sgst_rate = half_rate
            igst_rate = Decimal("0")
            cgst_amount = (taxable_value * cgst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            sgst_amount = (taxable_value * sgst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            igst_amount = Decimal("0")
        
        return {
            "cgst_rate": cgst_rate,
            "sgst_rate": sgst_rate,
            "igst_rate": igst_rate,
            "cgst_amount": cgst_amount,
            "sgst_amount": sgst_amount,
            "igst_amount": igst_amount,
            "total_tax": cgst_amount + sgst_amount + igst_amount,
        }
    
    @staticmethod
    def calculate_invoice_totals(lines: list[Dict[str, Any]]) -> Dict[str, Decimal]:
        """Aggregate totals from calculated lines.
        
        Input lines should have: taxable_value, cgst_amount, sgst_amount, igst_amount, line_total
        """
        quantize = Decimal("0.01")
        totals = {
            "subtotal": Decimal("0"),
            "discount_total": Decimal("0"),
            "taxable_total": Decimal("0"),
            "cgst_total": Decimal("0"),
            "sgst_total": Decimal("0"),
            "igst_total": Decimal("0"),
            "grand_total": Decimal("0"),
        }
        for line in lines:
            totals["subtotal"] += Decimal(str(line.get("gross", 0)))
            totals["discount_total"] += Decimal(str(line.get("discount_amount", 0)))
            totals["taxable_total"] += Decimal(str(line.get("taxable_value", 0)))
            totals["cgst_total"] += Decimal(str(line.get("cgst_amount", 0)))
            totals["sgst_total"] += Decimal(str(line.get("sgst_amount", 0)))
            totals["igst_total"] += Decimal(str(line.get("igst_amount", 0)))
            totals["grand_total"] += Decimal(str(line.get("line_total", 0)))
        
        return {k: v.quantize(quantize, rounding=ROUND_HALF_UP) for k, v in totals.items()}
```

```python
// File: backend/app/services/unit_service.py
import re
from sqlalchemy.orm import Session
from app.models.unit import Unit, UnitAlias, UnitCategory
from app.core.exceptions import ValidationException, NotFoundException
from app.services.audit_service import AuditService

class UnitService:
    @staticmethod
    def create_unit(db: Session, company_id: str, data: dict) -> Unit:
        # Validate formula if provided
        formula = data.get("conversion_formula")
        if formula:
            UnitService._validate_formula(formula)
        
        unit = Unit(
            company_id=company_id,
            unit_name=data["unit_name"],
            symbol=data["symbol"].upper(),
            internal_code=data.get("internal_code"),
            gst_unit_code=data.get("gst_unit_code"),
            category_id=data.get("category_id"),
            unit_type=data.get("unit_type", "CUSTOM"),
            base_unit_id=data.get("base_unit_id"),
            conversion_factor=data.get("conversion_factor"),
            conversion_formula=formula,
            precision=data.get("precision", 2),
            rounding_mode=data.get("rounding_mode", "HALF_UP"),
        )
        db.add(unit)
        db.commit()
        db.refresh(unit)
        AuditService.log(db, company_id, "UNIT", unit.id, "CREATED")
        return unit
    
    @staticmethod
    def _validate_formula(formula: str):
        # Safe validation: only allow numbers, operators, parentheses, and unit references
        cleaned = formula.strip().lstrip("=")
        # Allow: 0-9 . + - * / ^ ( ) and alphanumeric unit references
        if not re.match(r'^[\\d\\s\\.\\+\\-\\*\\/\\^\\(\\)A-Za-z_]+$', cleaned):
            raise ValidationException("Formula contains invalid characters")
        # Basic syntax check
        try:
            # We can't safely eval, so we just check parentheses balance
            if cleaned.count("(") != cleaned.count(")"):
                raise ValidationException("Unbalanced parentheses in formula")
        except Exception as e:
            raise ValidationException(f"Invalid formula: {str(e)}")
    
    @staticmethod
    def list_units(db: Session, company_id: str, search: str = None):
        query = db.query(Unit).filter(
            (Unit.company_id == company_id) | (Unit.is_predefined == True),
            Unit.is_active == True
        )
        if search:
            query = query.filter(Unit.unit_name.ilike(f"%{search}%") | Unit.symbol.ilike(f"%{search}%"))
        return query.order_by(Unit.unit_name).all()
    
    @staticmethod
    def get_unit(db: Session, unit_id: str, company_id: str) -> Unit:
        unit = db.query(Unit).filter(Unit.id == unit_id).first()
        if not unit:
            raise NotFoundException("Unit not found")
        if unit.company_id != company_id and not unit.is_predefined:
            raise ValidationException("Access denied")
        return unit

    @staticmethod
    def list_categories(db: Session):
        return db.query(UnitCategory).filter(UnitCategory.status == "ACTIVE").order_by(UnitCategory.name).all()

    @staticmethod
    def update_unit(db: Session, company_id: str, unit_id: str, data: dict) -> Unit:
        unit = UnitService.get_unit(db, unit_id, company_id)
        if unit.is_predefined:
            raise ValidationException("Cannot modify predefined units")
        
        formula = data.get("conversion_formula")
        if formula:
            UnitService._validate_formula(formula)
        
        for key, value in data.items():
            if hasattr(unit, key) and value is not None:
                if key == "symbol":
                    setattr(unit, key, value.upper())
                else:
                    setattr(unit, key, value)
        
        db.commit()
        db.refresh(unit)
        AuditService.log(db, company_id, "UNIT", unit.id, "UPDATED")
        return unit
    
    @staticmethod
    def delete_unit(db: Session, company_id: str, unit_id: str):
        unit = UnitService.get_unit(db, unit_id, company_id)
        if unit.is_predefined:
            raise ValidationException("Cannot delete predefined units")
            
        from app.models.item import Item
        # In actual implementation check for usage in invoice_lines as well
        in_use = db.query(Item).filter(Item.unit_id == unit_id).first()
        if in_use:
            unit.is_active = False
            db.commit()
            AuditService.log(db, company_id, "UNIT", unit.id, "DEACTIVATED")
        else:
            db.delete(unit)
            db.commit()
            AuditService.log(db, company_id, "UNIT", unit_id, "DELETED")
```

```python
// File: backend/app/utils/currency.py
def amount_in_words(amount: float) -> str:
    """Convert numeric amount to words (Indian numbering)."""
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
            "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
            "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    def convert_less_than_thousand(n):
        if n == 0:
            return ""
        elif n < 20:
            return ones[n]
        elif n < 100:
            return tens[n // 10] + ("" if n % 10 == 0 else " " + ones[n % 10])
        else:
            return ones[n // 100] + " Hundred" + ("" if n % 100 == 0 else " and " + convert_less_than_thousand(n % 100))
    
    if amount == 0:
        return "Zero Rupees Only"
    
    rupees = int(amount)
    paise = round((amount - rupees) * 100)
    
    result = ""
    if rupees > 0:
        crore = rupees // 10000000
        lakh = (rupees // 100000) % 100
        thousand = (rupees // 1000) % 100
        remainder = rupees % 1000
        
        parts = []
        if crore > 0:
            parts.append(convert_less_than_thousand(crore) + " Crore")
        if lakh > 0:
            parts.append(convert_less_than_thousand(lakh) + " Lakh")
        if thousand > 0:
            parts.append(convert_less_than_thousand(thousand) + " Thousand")
        if remainder > 0:
            parts.append(convert_less_than_thousand(remainder))
        
        result = " ".join(parts) + " Rupees"
    
    if paise > 0:
        if result:
            result += " and "
        result += convert_less_than_thousand(paise) + " Paise"
    
    return result + " Only"
```

```python
// File: backend/app/utils/dates.py
from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def format_ist(dt: datetime) -> str:
    from zoneinfo import ZoneInfo
    return dt.astimezone(ZoneInfo("Asia/Kolkata")).strftime("%d-%m-%Y %H:%M")
```

```python
// File: backend/app/utils/formula_engine.py
"""Safe formula evaluation engine for unit conversions.
Supports Excel-style formulas without arbitrary code execution.
"""
import re
import operator
import math
from decimal import Decimal, InvalidOperation
from typing import Dict, Any

class FormulaError(Exception):
    pass

class FormulaEngine:
    """Safe formula parser and evaluator for unit conversions.
    
    Supported syntax:
    - Numbers: 12, 0.5, 2.5
    - Operators: +, -, *, /, ^
    - Parentheses: ( )
    - Unit references: PCS, KG, BOX (resolved via context)
    - Functions: ROUND, SQRT
    """
    
    TOKEN_SPEC = [
        ("NUMBER", r"\d+(?:\.\d+)?"),
        ("NAME", r"[A-Za-z_][A-Za-z0-9_]*"),
        ("OP", r"[+\-*/^()]"),
        ("SKIP", r"[ \t]+"),
        ("MISMATCH", r"."),
    ]
    
    TOKEN_RE = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))
    
    @classmethod
    def tokenize(cls, formula: str):
        text = formula.strip().lstrip("=").strip()
        tokens = []
        for mo in cls.TOKEN_RE.finditer(text):
            kind = mo.lastgroup
            value = mo.group()
            if kind == "SKIP":
                continue
            elif kind == "MISMATCH":
                raise FormulaError(f"Unexpected character: {value}")
            tokens.append((kind, value))
        return tokens
    
    @classmethod
    def validate_syntax(cls, formula: str):
        tokens = cls.tokenize(formula)
        # Check parentheses balance
        parens = sum(1 for t in tokens if t[1] == "(") - sum(1 for t in tokens if t[1] == ")")
        if parens != 0:
            raise FormulaError("Unbalanced parentheses")
        # Check no consecutive operators (basic)
        ops = {"+", "-", "*", "/", "^"}
        for i in range(len(tokens) - 1):
            if tokens[i][1] in ops and tokens[i+1][1] in ops:
                if tokens[i+1][1] not in {"+", "-"}:  # unary allowed after operator
                    raise FormulaError(f"Consecutive operators: {tokens[i][1]} {tokens[i+1][1]}")
        return True
    
    @classmethod
    def evaluate(cls, formula: str, unit_values: Dict[str, Decimal]) -> Decimal:
        """Evaluate formula with given unit values.
        
        Example:
            formula = "=12*PCS"
            unit_values = {"PCS": Decimal("1")}
            result = Decimal("12")
        """
        cls.validate_syntax(formula)
        tokens = cls.tokenize(formula)
        
        # Convert to postfix (RPN) using shunting yard
        output = []
        stack = []
        precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        
        i = 0
        while i < len(tokens):
            kind, value = tokens[i]
            if kind == "NUMBER":
                output.append(Decimal(value))
            elif kind == "NAME":
                upper_val = value.upper()
                if upper_val in unit_values:
                    output.append(unit_values[upper_val])
                elif upper_val == "ROUND":
                    stack.append("ROUND")
                elif upper_val == "SQRT":
                    stack.append("SQRT")
                else:
                    raise FormulaError(f"Unknown reference: {value}")
            elif value == ",":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
            elif value == "(":
                stack.append(value)
            elif value == ")":
                while stack and stack[-1] != "(":
                    output.append(stack.pop())
                if not stack:
                    raise FormulaError("Mismatched parentheses")
                stack.pop()  # pop "("
                if stack and stack[-1] in {"ROUND", "SQRT"}:
                    output.append(stack.pop())
            elif kind == "OP":
                while (stack and stack[-1] != "(" and
                       stack[-1] in precedence and
                       precedence[stack[-1]] >= precedence.get(value, 0)):
                    output.append(stack.pop())
                stack.append(value)
            i += 1
        
        while stack:
            op = stack.pop()
            if op in {"(", ")"}:
                raise FormulaError("Mismatched parentheses")
            output.append(op)
        
        # Evaluate RPN
        eval_stack = []
        for token in output:
            if isinstance(token, Decimal):
                eval_stack.append(token)
            elif token == "+":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a + b)
            elif token == "-":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a - b)
            elif token == "*":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a * b)
            elif token == "/":
                b, a = eval_stack.pop(), eval_stack.pop()
                if b == 0:
                    raise FormulaError("Division by zero")
                eval_stack.append(a / b)
            elif token == "^":
                b, a = eval_stack.pop(), eval_stack.pop()
                eval_stack.append(a ** b)
            elif token == "ROUND":
                a = eval_stack.pop()
                eval_stack.append(a.quantize(Decimal("0.01")))
            elif token == "SQRT":
                a = eval_stack.pop()
                eval_stack.append(Decimal(str(math.sqrt(float(a)))))
        
        if len(eval_stack) != 1:
            raise FormulaError("Invalid formula expression")
        return eval_stack[0]


def validate_conversion_formula(formula: str, available_units: list[str]) -> dict:
    """Validate a unit conversion formula.
    
    Returns:
        {"valid": bool, "error": str|None, "normalized": str}
    """
    try:
        FormulaEngine.validate_syntax(formula)
        tokens = FormulaEngine.tokenize(formula)
        refs = {t[1].upper() for t in tokens if t[0] == "NAME"}
        funcs = {"ROUND", "SQRT"}
        unknown = refs - set(u.upper() for u in available_units) - funcs
        if unknown:
            return {"valid": False, "error": f"Unknown unit reference: {', '.join(unknown)}", "normalized": None}
        normalized = formula.strip().lstrip("=").strip().upper()
        return {"valid": True, "error": None, "normalized": normalized}
    except FormulaError as e:
        return {"valid": False, "error": str(e), "normalized": None}
```

```python
// File: backend/app/utils/gstin.py
import re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
GSTN_CODEPOINT_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def validate_gstin_format(gstin: str) -> bool:
    """Validate GSTIN format using regex."""
    if not gstin or len(gstin) != 15:
        return False
    return bool(GSTIN_REGEX.match(gstin.upper()))

def validate_gstin_checksum(gstin: str) -> bool:
    """Validate GSTIN checksum using the official algorithm."""
    gstin = gstin.upper()
    if len(gstin) != 15:
        return False
    check = gstin[-1]
    body = gstin[:-1]
    # Convert each char to numeric value: 0-9 -> 0-9, A-Z -> 10-35
    l = [int(c) if c.isdigit() else ord(c) - 55 for c in body]
    # Apply alternating weights (2,1,2,1... from left to right, or equivalently index%2+1)
    l = [val * (ind % 2 + 1) for (ind, val) in enumerate(l)]
    # For each weighted value: digit = (digit // 36) + (digit % 36)
    l = [(x // 36) + (x % 36) for x in l]
    csum = 36 - (sum(l) % 36)
    csum = str(csum) if csum < 10 else chr(csum + 55)
    return check == csum

def validate_gstin(gstin: str) -> dict:
    """Full GSTIN validation with component extraction."""
    normalized = gstin.upper().strip().replace(" ", "")
    result = {
        "normalized": normalized,
        "valid_format": False,
        "valid_checksum": False,
        "valid": False,
        "state_code": None,
        "pan": None,
        "registration_number": None,
        "default_code": None,
        "checksum": None,
    }
    if len(normalized) != 15:
        return result
    result["valid_format"] = validate_gstin_format(normalized)
    result["valid_checksum"] = validate_gstin_checksum(normalized)
    result["valid"] = result["valid_format"] and result["valid_checksum"]
    result["state_code"] = normalized[:2]
    result["pan"] = normalized[2:12]
    result["registration_number"] = normalized[12]
    result["default_code"] = normalized[13]
    result["checksum"] = normalized[14]
    return result

def extract_pan_from_gstin(gstin: str) -> str:
    """Extract PAN from GSTIN."""
    normalized = gstin.upper().strip().replace(" ", "")
    if len(normalized) >= 12:
        return normalized[2:12]
    return ""
```

```python
// File: backend/fix_slashes.py
import os
import glob
import re

directory = "/root/artha/backend/app/api/v1"

for filepath in glob.glob(os.path.join(directory, "*.py")):
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace @router.get("/") with @router.get("")
    content = re.sub(r'@router\.get\("/"\)', '@router.get("")', content)
    # Replace @router.post("/") with @router.post("")
    content = re.sub(r'@router\.post\("/"\)', '@router.post("")', content)
    # Replace @router.put("/") with @router.put("")
    content = re.sub(r'@router\.put\("/"\)', '@router.put("")', content)

    with open(filepath, 'w') as f:
        f.write(content)

print("Fixed trailing slashes!")
```

```sql
// File: backend/migrations/add_phase10_columns.sql
-- Phase 10: Business Identity & GST Validation
-- Run this if you have an existing database

ALTER TABLE companies ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE companies ADD COLUMN mobile_e164 VARCHAR(20);
ALTER TABLE companies ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE companies ADD COLUMN office_phone_e164 VARCHAR(20);
ALTER TABLE companies ADD COLUMN logo_url VARCHAR(500);

ALTER TABLE company_gst_details ADD COLUMN tan VARCHAR(10);

ALTER TABLE company_bank_accounts RENAME COLUMN account_type TO account_type_old;
ALTER TABLE company_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';

ALTER TABLE company_assets ADD COLUMN original_width INTEGER;
ALTER TABLE company_assets ADD COLUMN original_height INTEGER;
ALTER TABLE company_assets ADD COLUMN standardized BOOLEAN DEFAULT 0;

ALTER TABLE parties ADD COLUMN tan VARCHAR(10);
ALTER TABLE parties ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE parties ADD COLUMN mobile_e164 VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE parties ADD COLUMN office_phone_e164 VARCHAR(20);

ALTER TABLE party_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';
```

```sql
// File: backend/migrations/phase11_schema.sql
-- Phase 11: Schema additions
-- SQLite-compatible ALTER TABLE statements
-- Run ONCE on existing databases to add new columns added in Phase 10-11
-- Fresh installs: create_all() handles this automatically

-- Company: new contact/logo fields
ALTER TABLE companies ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE companies ADD COLUMN mobile_e164 VARCHAR(25);
ALTER TABLE companies ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE companies ADD COLUMN office_phone_e164 VARCHAR(25);
ALTER TABLE companies ADD COLUMN website VARCHAR(300);
ALTER TABLE companies ADD COLUMN logo_url VARCHAR(500);
ALTER TABLE companies ADD COLUMN logo_asset_id VARCHAR(36);

-- Company GST: TAN field
ALTER TABLE company_gst_details ADD COLUMN tan VARCHAR(10);

-- Parties: new contact fields
ALTER TABLE parties ADD COLUMN tan VARCHAR(10);
ALTER TABLE parties ADD COLUMN mobile_country_code VARCHAR(5) DEFAULT '+91';
ALTER TABLE parties ADD COLUMN mobile_e164 VARCHAR(25);
ALTER TABLE parties ADD COLUMN office_phone VARCHAR(20);
ALTER TABLE parties ADD COLUMN office_phone_country_code VARCHAR(5);
ALTER TABLE parties ADD COLUMN office_phone_e164 VARCHAR(25);

-- Party bank accounts: account type
ALTER TABLE party_bank_accounts ADD COLUMN account_type VARCHAR(30) DEFAULT 'CURRENT';

-- Company assets: standardization metadata
ALTER TABLE company_assets ADD COLUMN original_width INTEGER;
ALTER TABLE company_assets ADD COLUMN original_height INTEGER;
ALTER TABLE company_assets ADD COLUMN standardized BOOLEAN DEFAULT 0;
```

```toml
// File: backend/pyproject.toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "gst-billing-backend"
version = "1.0.0"
description = "GST Billing Web Application Backend"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.111.0",
    "uvicorn[standard]>=0.30.0",
    "sqlalchemy>=2.0.30",
    "alembic>=1.13.0",
    "pydantic>=2.7.0",
    "pydantic-settings>=2.3.0",
    "argon2-cffi>=23.1.0",
    "python-multipart>=0.0.9",
    "python-jose[cryptography]>=3.3.0",
    "httpx>=0.27.0",
    "pytest>=8.2.0",
    "pytest-asyncio>=0.23.0",
    "aiofiles>=23.2.0",
    "email-validator>=2.1.0",
    "reportlab>=4.0.0",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
```

```json
// File: frontend/.oxlintrc.json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

```
// File: frontend/Dockerfile
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# VITE_API_URL defaults to /api/v1 for production (Nginx proxy)
ARG VITE_API_URL=/api/v1
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
# Use our custom nginx config (handles /api proxy + SPA routing)
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```markdown
// File: frontend/README.md
# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some Oxlint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the Oxlint configuration

If you are developing a production application, we recommend enabling type-aware lint rules by installing `oxlint-tsgolint` and editing `.oxlintrc.json`:

```json
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["react", "typescript", "oxc"],
  "options": {
    "typeAware": true
  },
  "rules": {
    "react/rules-of-hooks": "error",
    "react/only-export-components": ["warn", { "allowConstantExport": true }]
  }
}
```

See the [Oxlint rules documentation](https://oxc.rs/docs/guide/usage/linter/rules) for the full list of rules and categories.
```

```html
// File: frontend/index.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>frontend</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

```conf
// File: frontend/nginx.conf
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    # Proxy /api/* to the backend service
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
        # Pass CORS preflight through to FastAPI
        proxy_pass_header Access-Control-Allow-Origin;
    }

    # Static assets — cache aggressively
    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://backend:8000/health;
        proxy_set_header Host $host;
    }

    # SPA routing — all other routes serve index.html
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

```json
// File: frontend/package.json
{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "oxlint",
    "preview": "vite preview"
  },
  "dependencies": {
    "@hookform/resolvers": "^5.7.1",
    "@tanstack/react-query": "^5.101.4",
    "@tanstack/react-table": "^8.21.3",
    "axios": "^1.19.0",
    "libphonenumber-js": "^1.13.11",
    "react": "^19.2.8",
    "react-dom": "^19.2.8",
    "react-hook-form": "^7.85.0",
    "react-router-dom": "^7.18.2",
    "zod": "^4.4.3"
  },
  "devDependencies": {
    "@radix-ui/react-checkbox": "^1.3.11",
    "@radix-ui/react-dialog": "^1.1.23",
    "@radix-ui/react-dropdown-menu": "^2.1.24",
    "@radix-ui/react-label": "^2.1.15",
    "@radix-ui/react-select": "^2.3.7",
    "@radix-ui/react-separator": "^1.1.15",
    "@radix-ui/react-slot": "^1.3.3",
    "@radix-ui/react-switch": "^1.3.7",
    "@radix-ui/react-toast": "^1.2.23",
    "@tailwindcss/postcss": "^4.3.3",
    "@tailwindcss/vite": "^4.3.3",
    "@types/node": "^24.13.3",
    "@types/react": "^19.2.17",
    "@types/react-dom": "^19.2.3",
    "@vitejs/plugin-react": "^6.0.4",
    "autoprefixer": "^10.5.4",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "lucide-react": "^1.31.0",
    "oxlint": "^1.75.0",
    "postcss": "^8.5.26",
    "prettier": "^3.9.6",
    "tailwind-merge": "^3.6.0",
    "tailwindcss": "^4.3.3",
    "typescript": "~6.0.2",
    "vite": "^8.2.0"
  }
}
```

```javascript
// File: frontend/postcss.config.js
export default {
  plugins: {
    '@tailwindcss/postcss': {},
    autoprefixer: {},
  },
}
```

```xml
// File: frontend/public/favicon.svg
<svg xmlns="http://www.w3.org/2000/svg" width="48" height="46" fill="none" viewBox="0 0 48 46"><path fill="#863bff" d="M25.946 44.938c-.664.845-2.021.375-2.021-.698V33.937a2.26 2.26 0 0 0-2.262-2.262H10.287c-.92 0-1.456-1.04-.92-1.788l7.48-10.471c1.07-1.497 0-3.578-1.842-3.578H1.237c-.92 0-1.456-1.04-.92-1.788L10.013.474c.214-.297.556-.474.92-.474h28.894c.92 0 1.456 1.04.92 1.788l-7.48 10.471c-1.07 1.498 0 3.579 1.842 3.579h11.377c.943 0 1.473 1.088.89 1.83L25.947 44.94z" style="fill:#863bff;fill:color(display-p3 .5252 .23 1);fill-opacity:1"/><mask id="a" width="48" height="46" x="0" y="0" maskUnits="userSpaceOnUse" style="mask-type:alpha"><path fill="#000" d="M25.842 44.938c-.664.844-2.021.375-2.021-.698V33.937a2.26 2.26 0 0 0-2.262-2.262H10.183c-.92 0-1.456-1.04-.92-1.788l7.48-10.471c1.07-1.498 0-3.579-1.842-3.579H1.133c-.92 0-1.456-1.04-.92-1.787L9.91.473c.214-.297.556-.474.92-.474h28.894c.92 0 1.456 1.04.92 1.788l-7.48 10.471c-1.07 1.498 0 3.578 1.842 3.578h11.377c.943 0 1.473 1.088.89 1.832L25.843 44.94z" style="fill:#000;fill-opacity:1"/></mask><g mask="url(#a)"><g filter="url(#b)"><ellipse cx="5.508" cy="14.704" fill="#ede6ff" rx="5.508" ry="14.704" style="fill:#ede6ff;fill:color(display-p3 .9275 .9033 1);fill-opacity:1" transform="matrix(.00324 1 1 -.00324 -4.47 31.516)"/></g><g filter="url(#c)"><ellipse cx="10.399" cy="29.851" fill="#ede6ff" rx="10.399" ry="29.851" style="fill:#ede6ff;fill:color(display-p3 .9275 .9033 1);fill-opacity:1" transform="matrix(.00324 1 1 -.00324 -39.328 7.883)"/></g><g filter="url(#d)"><ellipse cx="5.508" cy="30.487" fill="#7e14ff" rx="5.508" ry="30.487" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(89.814 -25.913 -14.639)scale(1 -1)"/></g><g filter="url(#e)"><ellipse cx="5.508" cy="30.599" fill="#7e14ff" rx="5.508" ry="30.599" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(89.814 -32.644 -3.334)scale(1 -1)"/></g><g filter="url(#f)"><ellipse cx="5.508" cy="30.599" fill="#7e14ff" rx="5.508" ry="30.599" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="matrix(.00324 1 1 -.00324 -34.34 30.47)"/></g><g filter="url(#g)"><ellipse cx="14.072" cy="22.078" fill="#ede6ff" rx="14.072" ry="22.078" style="fill:#ede6ff;fill:color(display-p3 .9275 .9033 1);fill-opacity:1" transform="rotate(93.35 24.506 48.493)scale(-1 1)"/></g><g filter="url(#h)"><ellipse cx="3.47" cy="21.501" fill="#7e14ff" rx="3.47" ry="21.501" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(89.009 28.708 47.59)scale(-1 1)"/></g><g filter="url(#i)"><ellipse cx="3.47" cy="21.501" fill="#7e14ff" rx="3.47" ry="21.501" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(89.009 28.708 47.59)scale(-1 1)"/></g><g filter="url(#j)"><ellipse cx=".387" cy="8.972" fill="#7e14ff" rx="4.407" ry="29.108" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(39.51 .387 8.972)"/></g><g filter="url(#k)"><ellipse cx="47.523" cy="-6.092" fill="#7e14ff" rx="4.407" ry="29.108" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(37.892 47.523 -6.092)"/></g><g filter="url(#l)"><ellipse cx="41.412" cy="6.333" fill="#47bfff" rx="5.971" ry="9.665" style="fill:#47bfff;fill:color(display-p3 .2799 .748 1);fill-opacity:1" transform="rotate(37.892 41.412 6.333)"/></g><g filter="url(#m)"><ellipse cx="-1.879" cy="38.332" fill="#7e14ff" rx="4.407" ry="29.108" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(37.892 -1.88 38.332)"/></g><g filter="url(#n)"><ellipse cx="-1.879" cy="38.332" fill="#7e14ff" rx="4.407" ry="29.108" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(37.892 -1.88 38.332)"/></g><g filter="url(#o)"><ellipse cx="35.651" cy="29.907" fill="#7e14ff" rx="4.407" ry="29.108" style="fill:#7e14ff;fill:color(display-p3 .4922 .0767 1);fill-opacity:1" transform="rotate(37.892 35.651 29.907)"/></g><g filter="url(#p)"><ellipse cx="38.418" cy="32.4" fill="#47bfff" rx="5.971" ry="15.297" style="fill:#47bfff;fill:color(display-p3 .2799 .748 1);fill-opacity:1" transform="rotate(37.892 38.418 32.4)"/></g></g><defs><filter id="b" width="60.045" height="41.654" x="-19.77" y="16.149" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="7.659"/></filter><filter id="c" width="90.34" height="51.437" x="-54.613" y="-7.533" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="7.659"/></filter><filter id="d" width="79.355" height="29.4" x="-49.64" y="2.03" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="e" width="79.579" height="29.4" x="-45.045" y="20.029" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="f" width="79.579" height="29.4" x="-43.513" y="21.178" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="g" width="74.749" height="58.852" x="15.756" y="-17.901" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="7.659"/></filter><filter id="h" width="61.377" height="25.362" x="23.548" y="2.284" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="i" width="61.377" height="25.362" x="23.548" y="2.284" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="j" width="56.045" height="63.649" x="-27.636" y="-22.853" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="k" width="54.814" height="64.646" x="20.116" y="-38.415" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="l" width="33.541" height="35.313" x="24.641" y="-11.323" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="m" width="54.814" height="64.646" x="-29.286" y="6.009" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="n" width="54.814" height="64.646" x="-29.286" y="6.009" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="o" width="54.814" height="64.646" x="8.244" y="-2.416" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter><filter id="p" width="39.409" height="43.623" x="18.713" y="10.588" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17158" stdDeviation="4.596"/></filter></defs></svg>
```

```xml
// File: frontend/public/icons.svg
<svg xmlns="http://www.w3.org/2000/svg">
  <symbol id="bluesky-icon" viewBox="0 0 16 17">
    <g clip-path="url(#bluesky-clip)"><path fill="#08060d" d="M7.75 7.735c-.693-1.348-2.58-3.86-4.334-5.097-1.68-1.187-2.32-.981-2.74-.79C.188 2.065.1 2.812.1 3.251s.241 3.602.398 4.13c.52 1.744 2.367 2.333 4.07 2.145-2.495.37-4.71 1.278-1.805 4.512 3.196 3.309 4.38-.71 4.987-2.746.608 2.036 1.307 5.91 4.93 2.746 2.72-2.746.747-4.143-1.747-4.512 1.702.189 3.55-.4 4.07-2.145.156-.528.397-3.691.397-4.13s-.088-1.186-.575-1.406c-.42-.19-1.06-.395-2.741.79-1.755 1.24-3.64 3.752-4.334 5.099"/></g>
    <defs><clipPath id="bluesky-clip"><path fill="#fff" d="M.1.85h15.3v15.3H.1z"/></clipPath></defs>
  </symbol>
  <symbol id="discord-icon" viewBox="0 0 20 19">
    <path fill="#08060d" d="M16.224 3.768a14.5 14.5 0 0 0-3.67-1.153c-.158.286-.343.67-.47.976a13.5 13.5 0 0 0-4.067 0c-.128-.306-.317-.69-.476-.976A14.4 14.4 0 0 0 3.868 3.77C1.546 7.28.916 10.703 1.231 14.077a14.7 14.7 0 0 0 4.5 2.306q.545-.748.965-1.587a9.5 9.5 0 0 1-1.518-.74q.191-.14.372-.293c2.927 1.369 6.107 1.369 8.999 0q.183.152.372.294-.723.437-1.52.74.418.838.963 1.588a14.6 14.6 0 0 0 4.504-2.308c.37-3.911-.63-7.302-2.644-10.309m-9.13 8.234c-.878 0-1.599-.82-1.599-1.82 0-.998.705-1.82 1.6-1.82.894 0 1.614.82 1.599 1.82.001 1-.705 1.82-1.6 1.82m5.91 0c-.878 0-1.599-.82-1.599-1.82 0-.998.705-1.82 1.6-1.82.893 0 1.614.82 1.599 1.82 0 1-.706 1.82-1.6 1.82"/>
  </symbol>
  <symbol id="documentation-icon" viewBox="0 0 21 20">
    <path fill="none" stroke="#aa3bff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.35" d="m15.5 13.333 1.533 1.322c.645.555.967.833.967 1.178s-.322.623-.967 1.179L15.5 18.333m-3.333-5-1.534 1.322c-.644.555-.966.833-.966 1.178s.322.623.966 1.179l1.534 1.321"/>
    <path fill="none" stroke="#aa3bff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.35" d="M17.167 10.836v-4.32c0-1.41 0-2.117-.224-2.68-.359-.906-1.118-1.621-2.08-1.96-.599-.21-1.349-.21-2.848-.21-2.623 0-3.935 0-4.983.369-1.684.591-3.013 1.842-3.641 3.428C3 6.449 3 7.684 3 10.154v2.122c0 2.558 0 3.838.706 4.726q.306.383.713.671c.76.536 1.79.64 3.581.66"/>
    <path fill="none" stroke="#aa3bff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.35" d="M3 10a2.78 2.78 0 0 1 2.778-2.778c.555 0 1.209.097 1.748-.047.48-.129.854-.503.982-.982.145-.54.048-1.194.048-1.749a2.78 2.78 0 0 1 2.777-2.777"/>
  </symbol>
  <symbol id="github-icon" viewBox="0 0 19 19">
    <path fill="#08060d" fill-rule="evenodd" d="M9.356 1.85C5.05 1.85 1.57 5.356 1.57 9.694a7.84 7.84 0 0 0 5.324 7.44c.387.079.528-.168.528-.376 0-.182-.013-.805-.013-1.454-2.165.467-2.616-.935-2.616-.935-.349-.91-.864-1.143-.864-1.143-.71-.48.051-.48.051-.48.787.051 1.2.805 1.2.805.695 1.194 1.817.857 2.268.649.064-.507.27-.857.49-1.052-1.728-.182-3.545-.857-3.545-3.87 0-.857.31-1.558.8-2.104-.078-.195-.349-1 .077-2.078 0 0 .657-.208 2.14.805a7.5 7.5 0 0 1 1.946-.26c.657 0 1.328.092 1.946.26 1.483-1.013 2.14-.805 2.14-.805.426 1.078.155 1.883.078 2.078.502.546.799 1.247.799 2.104 0 3.013-1.818 3.675-3.558 3.87.284.247.528.714.528 1.454 0 1.052-.012 1.896-.012 2.156 0 .208.142.455.528.377a7.84 7.84 0 0 0 5.324-7.441c.013-4.338-3.48-7.844-7.773-7.844" clip-rule="evenodd"/>
  </symbol>
  <symbol id="social-icon" viewBox="0 0 20 20">
    <path fill="none" stroke="#aa3bff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.35" d="M12.5 6.667a4.167 4.167 0 1 0-8.334 0 4.167 4.167 0 0 0 8.334 0"/>
    <path fill="none" stroke="#aa3bff" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.35" d="M2.5 16.667a5.833 5.833 0 0 1 8.75-5.053m3.837.474.513 1.035c.07.144.257.282.414.309l.93.155c.596.1.736.536.307.965l-.723.73a.64.64 0 0 0-.152.531l.207.903c.164.715-.213.991-.84.618l-.872-.52a.63.63 0 0 0-.577 0l-.872.52c-.624.373-1.003.094-.84-.618l.207-.903a.64.64 0 0 0-.152-.532l-.723-.729c-.426-.43-.289-.864.306-.964l.93-.156a.64.64 0 0 0 .412-.31l.513-1.034c.28-.562.735-.562 1.012 0"/>
  </symbol>
  <symbol id="x-icon" viewBox="0 0 19 19">
    <path fill="#08060d" fill-rule="evenodd" d="M1.893 1.98c.052.072 1.245 1.769 2.653 3.77l2.892 4.114c.183.261.333.48.333.486s-.068.089-.152.183l-.522.593-.765.867-3.597 4.087c-.375.426-.734.834-.798.905a1 1 0 0 0-.118.148c0 .01.236.017.664.017h.663l.729-.83c.4-.457.796-.906.879-.999a692 692 0 0 0 1.794-2.038c.034-.037.301-.34.594-.675l.551-.624.345-.392a7 7 0 0 1 .34-.374c.006 0 .93 1.306 2.052 2.903l2.084 2.965.045.063h2.275c1.87 0 2.273-.003 2.266-.021-.008-.02-1.098-1.572-3.894-5.547-2.013-2.862-2.28-3.246-2.273-3.266.008-.019.282-.332 2.085-2.38l2-2.274 1.567-1.782c.022-.028-.016-.03-.65-.03h-.674l-.3.342a871 871 0 0 1-1.782 2.025c-.067.075-.405.458-.75.852a100 100 0 0 1-.803.91c-.148.172-.299.344-.99 1.127-.304.343-.32.358-.345.327-.015-.019-.904-1.282-1.976-2.808L6.365 1.85H1.8zm1.782.91 8.078 11.294c.772 1.08 1.413 1.973 1.425 1.984.016.017.241.02 1.05.017l1.03-.004-2.694-3.766L7.796 5.75 5.722 2.852l-1.039-.004-1.039-.004z" clip-rule="evenodd"/>
  </symbol>
</svg>
```

```css
// File: frontend/src/App.css
.counter {
  font-size: 16px;
  padding: 5px 10px;
  border-radius: 5px;
  color: var(--accent);
  background: var(--accent-bg);
  border: 2px solid transparent;
  transition: border-color 0.3s;
  margin-bottom: 24px;

  &:hover {
    border-color: var(--accent-border);
  }
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

.hero {
  position: relative;

  .base,
  .framework,
  .vite {
    inset-inline: 0;
    margin: 0 auto;
  }

  .base {
    width: 170px;
    position: relative;
    z-index: 0;
  }

  .framework,
  .vite {
    position: absolute;
  }

  .framework {
    z-index: 1;
    top: 34px;
    height: 28px;
    transform: perspective(2000px) rotateZ(300deg) rotateX(44deg) rotateY(39deg)
      scale(1.4);
  }

  .vite {
    z-index: 0;
    top: 107px;
    height: 26px;
    width: auto;
    transform: perspective(2000px) rotateZ(300deg) rotateX(40deg) rotateY(39deg)
      scale(0.8);
  }
}

#center {
  display: flex;
  flex-direction: column;
  gap: 25px;
  place-content: center;
  place-items: center;
  flex-grow: 1;

  @media (max-width: 1024px) {
    padding: 32px 20px 24px;
    gap: 18px;
  }
}

#next-steps {
  display: flex;
  border-top: 1px solid var(--border);
  text-align: left;

  & > div {
    flex: 1 1 0;
    padding: 32px;
    @media (max-width: 1024px) {
      padding: 24px 20px;
    }
  }

  .icon {
    margin-bottom: 16px;
    width: 22px;
    height: 22px;
  }

  @media (max-width: 1024px) {
    flex-direction: column;
    text-align: center;
  }
}

#docs {
  border-right: 1px solid var(--border);

  @media (max-width: 1024px) {
    border-right: none;
    border-bottom: 1px solid var(--border);
  }
}

#next-steps ul {
  list-style: none;
  padding: 0;
  display: flex;
  gap: 8px;
  margin: 32px 0 0;

  .logo {
    height: 18px;
  }

  a {
    color: var(--text-h);
    font-size: 16px;
    border-radius: 6px;
    background: var(--social-bg);
    display: flex;
    padding: 6px 12px;
    align-items: center;
    gap: 8px;
    text-decoration: none;
    transition: box-shadow 0.3s;

    &:hover {
      box-shadow: var(--shadow);
    }
    .button-icon {
      height: 18px;
      width: 18px;
    }
  }

  @media (max-width: 1024px) {
    margin-top: 20px;
    flex-wrap: wrap;
    justify-content: center;

    li {
      flex: 1 1 calc(50% - 8px);
    }

    a {
      width: 100%;
      justify-content: center;
      box-sizing: border-box;
    }
  }
}

#spacer {
  height: 88px;
  border-top: 1px solid var(--border);
  @media (max-width: 1024px) {
    height: 48px;
  }
}

.ticks {
  position: relative;
  width: 100%;

  &::before,
  &::after {
    content: '';
    position: absolute;
    top: -4.5px;
    border: 5px solid transparent;
  }

  &::before {
    left: 0;
    border-left-color: var(--border);
  }
  &::after {
    right: 0;
    border-right-color: var(--border);
  }
}
```

```tsx
// File: frontend/src/App.tsx
import { Outlet } from 'react-router-dom';

function App() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      <main className="flex-grow">
        <Outlet />
      </main>
    </div>
  );
}

export default App;
```

```typescript
// File: frontend/src/api/adjustmentNotes.ts
import { apiClient } from './client';

export interface AdjustmentNoteLineCreate {
  item_id?: string | null;
  item_name_snapshot: string;
  description?: string | null;
  quantity: number;
  unit_id: string;
  unit_snapshot: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface AdjustmentNoteCreateRequest {
  note_type: 'CREDIT_NOTE' | 'DEBIT_NOTE';
  source_type?: string | null;
  source_id?: string | null;
  source_number?: string | null;
  party_id: string;
  party_role: 'CUSTOMER' | 'SUPPLIER';
  note_date: string;
  reason_code: string;
  reason_description?: string | null;
  tax_treatment: 'GST' | 'WITHOUT_GST';
  place_of_supply: string;
  lines: AdjustmentNoteLineCreate[];
}

export interface AdjustmentNoteResponse {
  id: string;
  note_number: string;
  note_type: 'CREDIT_NOTE' | 'DEBIT_NOTE';
  source_type?: string | null;
  source_id?: string | null;
  source_number?: string | null;
  party_id: string;
  party_role: 'CUSTOMER' | 'SUPPLIER';
  note_date: string;
  reason_code: string;
  reason_description?: string | null;
  tax_treatment: 'GST' | 'WITHOUT_GST';
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  status: string;
  lines: any[];
  created_at: string;
}

export const adjustmentNotesApi = {
  create: async (data: AdjustmentNoteCreateRequest) => {
    const response = await apiClient.post<AdjustmentNoteResponse>('/adjustment-notes', data);
    return response.data;
  },
  getAll: async (note_type?: string) => {
    const params = new URLSearchParams();
    if (note_type) params.append('note_type', note_type);
    const response = await apiClient.get<{items: AdjustmentNoteResponse[], total: number}>(`/adjustment-notes?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<AdjustmentNoteResponse>(`/adjustment-notes/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/approve`, {});
    return response.data;
  },
  post: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/post`, {});
    return response.data;
  },
  cancel: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/cancel`, {});
    return response.data;
  },
  reverse: async (id: string) => {
    const response = await apiClient.post<AdjustmentNoteResponse>(`/adjustment-notes/${id}/reverse`, {});
    return response.data;
  },
  getPdf: async (id: string) => {
    const response = await apiClient.get(`/adjustment-notes/${id}/pdf`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    window.open(url, '_blank');
  }
};
```

```typescript
// File: frontend/src/api/auth.ts
import { apiClient } from './client';

export interface SetupRequest {
  company_name: string;
  ownership_type: string;
  mobile: string;
  mobile_country_code?: string;
  mobile_e164?: string;
  office_phone?: string;
  office_phone_country_code?: string;
  office_phone_e164?: string;
  email: string;
  website?: string;
  authorized_person_name: string;
  authorized_person_designation?: string;
  gst_registered: boolean;
  gstin?: string;
  tan?: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  district?: string;
  state: string;
  state_code: string;
  pincode: string;
  country: string;
  bank_account_holder_name?: string;
  bank_account_number?: string;
  bank_ifsc?: string;
  bank_name?: string;
  bank_branch?: string;
  bank_account_type?: string;
  pin: string;
  confirm_pin: string;
}

export interface LoginRequest {
  pin: string;
}

export interface PinChangeRequest {
  old_pin: string;
  new_pin: string;
  confirm_pin: string;
}

export const authApi = {
  setup: async (data: SetupRequest) => {
    const response = await apiClient.post('/auth/setup', data);
    return response.data;
  },
  login: async (data: LoginRequest) => {
    const response = await apiClient.post('/auth/login', data);
    return response.data;
  },
  changePin: async (data: PinChangeRequest) => {
    const response = await apiClient.post('/auth/pin-change', data);
    return response.data;
  },
  logout: async () => {
    const response = await apiClient.post('/auth/logout');
    return response.data;
  },
  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/boqs.ts
import { apiClient } from './client';

export interface BOQLineCreate {
  parent_line_id?: string | null;
  section?: string | null;
  item_type: string;
  item_id?: string | null;
  description: string;
  specification?: string | null;
  quantity: number;
  unit_id?: string | null;
  unit_snapshot?: string | null;
  quantity_formula?: string | null;
  estimated_rate?: number;
  remarks?: string | null;
  sort_order?: number;
}

export interface BOQCreateRequest {
  project_name?: string | null;
  party_id?: string | null;
  boq_date: string;
  notes?: string | null;
  lines: BOQLineCreate[];
}

export interface BOQLineResponse {
  id: string;
  parent_line_id: string | null;
  section: string | null;
  item_type: string;
  item_id: string | null;
  description: string;
  specification: string | null;
  quantity: number;
  unit_id: string | null;
  unit_snapshot: string | null;
  quantity_formula: string | null;
  estimated_rate: number;
  estimated_amount: number;
  remarks: string | null;
  sort_order: number;
}

export interface BOQResponse {
  id: string;
  boq_number: string | null;
  project_name: string | null;
  party_id: string | null;
  boq_date: string;
  version: number;
  status: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
  lines: BOQLineResponse[];
}

export const boqsApi = {
  create: async (data: BOQCreateRequest) => {
    const response = await apiClient.post<BOQResponse>('/boqs', data);
    return response.data;
  },
  getAll: async () => {
    const response = await apiClient.get<{items: BOQResponse[], total: number}>('/boqs');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<BOQResponse>(`/boqs/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<BOQResponse>(`/boqs/${id}/approve`, {});
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/client.ts
import axios, { AxiosError } from 'axios';

// Production (via Nginx proxy): /api/v1 — same origin, no CORS
// Development: http://localhost:8000/api/v1 (set in .env.development)
const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.dispatchEvent(new Event('unauthorized'));
    }

    const customError = {
      message: 'An unexpected error occurred',
      code: 'UNKNOWN_ERROR',
      fields: {} as Record<string, string>,
      status: error.response?.status || 500,
    };

    if (error.response?.data) {
      const data = error.response.data as any;
      if (data.detail && Array.isArray(data.detail)) {
        customError.message = 'Validation failed';
        customError.code = 'VALIDATION_ERROR';
        data.detail.forEach((err: any) => {
          customError.fields[err.loc.join('.')] = err.msg;
        });
      } else if (data.error) {
        customError.message = data.error.message || data.message || 'An error occurred';
        customError.code = data.error.code || 'API_ERROR';
      } else if (data.message) {
        customError.message = data.message;
        customError.code = data.code || 'API_ERROR';
      }
    }

    return Promise.reject(customError);
  }
);
```

```typescript
// File: frontend/src/api/company.ts
import { apiClient } from './client';

export interface CompanyDetail {
  id: string;
  company_name: string;
  legal_name?: string;
  trade_name?: string;
  ownership_type: string;
  status: string;
  mobile: string;
  mobile_country_code?: string;
  office_phone?: string;
  office_phone_country_code?: string;
  email: string;
  website?: string;
  authorized_person_name: string;
  logo_url?: string;
  gst_details?: {
    id: string;
    gstin?: string;
    state_code?: string;
    state_name?: string;
    pan?: string;
    tan?: string;
    gstin_validation_status: string;
  };
  bank_accounts: Array<{
    id: string;
    account_holder_name: string;
    account_number: string;
    ifsc: string;
    bank_name?: string;
    branch: string;
    account_type: string;
    is_primary: boolean;
  }>;
}

export const companyApi = {
  get: async (): Promise<CompanyDetail> => {
    const response = await apiClient.get<{ data: CompanyDetail }>('/company/');
    return (response.data as any).data;
  },
  update: async (data: Partial<CompanyDetail>): Promise<CompanyDetail> => {
    const response = await apiClient.put<{ data: CompanyDetail }>('/company/', data);
    return (response.data as any).data;
  },
  uploadLogo: async (file: File): Promise<{ logo_url: string; asset_id: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<{ data: { logo_url: string; asset_id: string } }>('/company/logo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return (response.data as any).data;
  },
};
```

```typescript
// File: frontend/src/api/estimates.ts
import { apiClient } from './client';

export interface EstimateLineCreate {
  item_name_snapshot: string;
  item_type?: string;
  quantity: number;
  unit_snapshot?: string;
  cost_rate?: number;
  markup_percent?: number;
}

export interface EstimateCreateRequest {
  boq_id?: string | null;
  party_id?: string | null;
  estimate_date: string;
  valid_until?: string | null;
  lines: EstimateLineCreate[];
}

export interface EstimateLineResponse {
  id: string;
  item_name_snapshot: string;
  item_type: string;
  quantity: number;
  unit_snapshot: string | null;
  cost_rate: number;
  cost_amount: number;
  markup_percent: number;
  markup_amount: number;
  selling_rate: number;
  selling_amount: number;
}

export interface EstimateResponse {
  id: string;
  estimate_number: string | null;
  boq_id: string | null;
  party_id: string | null;
  estimate_date: string;
  valid_until: string | null;
  version: number;
  status: string;
  material_cost: number;
  labour_cost: number;
  service_cost: number;
  other_cost: number;
  total_cost: number;
  markup_amount: number;
  estimated_selling_value: number;
  gst_total: number;
  grand_total: number;
  created_at: string;
  updated_at: string;
  lines: EstimateLineResponse[];
}

export const estimatesApi = {
  create: async (data: EstimateCreateRequest) => {
    const response = await apiClient.post<EstimateResponse>('/estimates', data);
    return response.data;
  },
  getAll: async () => {
    const response = await apiClient.get<{items: EstimateResponse[], total: number}>('/estimates');
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<EstimateResponse>(`/estimates/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<EstimateResponse>(`/estimates/${id}/approve`, {});
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/gst.ts
import { apiClient } from './client';

export interface GSTINValidationResponse {
  gstin: string;
  valid: boolean;
  validLength: boolean;
  validStructure: boolean;
  validStateCode: boolean;
  validChecksum: boolean;
  errors: string[];
  level: string;
  parsed?: {
    stateCode: string;
    stateName: string | null;
    pan: string;
    entityNumber: string;
    defaultCharacter: string;
    checkDigit: string;
  };
}

export interface GSTState {
  code: string;
  name: string;
  isUnionTerritory: boolean;
}

export const gstApi = {
  validate: async (gstin: string): Promise<GSTINValidationResponse> => {
    const response = await apiClient.get<{ data: GSTINValidationResponse }>(`/gst/validate/${encodeURIComponent(gstin)}`);
    return (response.data as any).data;
  },
  getStates: async (): Promise<GSTState[]> => {
    const response = await apiClient.get<{ data: GSTState[] }>('/gst/states');
    return (response.data as any).data;
  },
};
```

```typescript
// File: frontend/src/api/invoices.ts
import { apiClient } from './client';

export interface InvoiceLineCreate {
  item_id?: string | null;
  item_name: string;
  description?: string | null;
  hsn_sac?: string | null;
  quantity: number;
  unit_id: string;
  unit_name: string;
  unit_symbol: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface InvoiceCreateRequest {
  invoice_type?: string;
  invoice_date: string;
  customer_id: string;
  place_of_supply: string;
  lines: InvoiceLineCreate[];
  notes?: string | null;
  terms?: string | null;
}

export interface InvoiceCalculateRequest {
  customer_id?: string | null;
  place_of_supply: string;
  lines: InvoiceLineCreate[];
}

export interface InvoiceCalculateResponse {
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  amount_in_words?: string | null;
  lines: any[];
}

export interface InvoiceResponse {
  id: string;
  invoice_number: string;
  invoice_type: string;
  transaction_type: string;
  invoice_date: string;
  customer_id: string;
  customer_name_snapshot: string;
  place_of_supply: string;
  tax_treatment?: string;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  amount_in_words?: string | null;
  invoice_status: string;
  payment_status: string;
  notes?: string | null;
  lines: any[];
  created_at: string;
}

export const invoicesApi = {
  calculate: async (data: InvoiceCalculateRequest) => {
    const response = await apiClient.post<InvoiceCalculateResponse>('/invoices/calculate', data);
    return response.data;
  },
  create: async (data: InvoiceCreateRequest) => {
    const response = await apiClient.post<InvoiceResponse>('/invoices', data);
    return response.data;
  },
  getAll: async (transaction_type?: string) => {
    const params = new URLSearchParams();
    if (transaction_type) params.append('transaction_type', transaction_type);
    const response = await apiClient.get<{items: InvoiceResponse[], total: number}>(`/invoices?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<InvoiceResponse>(`/invoices/${id}`);
    return response.data;
  },
  finalize: async (id: string) => {
    const response = await apiClient.post<InvoiceResponse>(`/invoices/${id}/finalize`, {});
    return response.data;
  },
  cancel: async (id: string, reason: string) => {
    const response = await apiClient.post<InvoiceResponse>(`/invoices/${id}/cancel`, { cancel_reason: reason });
    return response.data;
  },
  getPdf: async (id: string) => {
    const response = await apiClient.get(`/invoices/${id}/pdf`, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
    window.open(url, '_blank');
  }
};
```

```typescript
// File: frontend/src/api/items.ts
import { apiClient } from './client';

export interface Item {
  id: number;
  type: string;
  sku: string | null;
  name: string;
  description: string | null;
  hsn_sac: string | null;
  gst_rate: number;
  cess_rate: number;
  sale_price: number;
  purchase_price: number;
  unit_id: number;
  stock_quantity: number;
  low_stock_warning: number;
  is_active: boolean;
}

export interface ItemCreateRequest {
  type: string;
  sku?: string | null;
  name: string;
  description?: string | null;
  hsn_sac?: string | null;
  gst_rate: number;
  cess_rate?: number;
  sale_price: number;
  purchase_price: number;
  unit_id: number;
  stock_quantity?: number;
  low_stock_warning?: number;
  is_active?: boolean;
}

export const itemsApi = {
  getAll: async () => {
    const response = await apiClient.get<Item[]>('/items');
    return response.data;
  },
  create: async (data: ItemCreateRequest) => {
    const response = await apiClient.post<Item>('/items', data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/items/${id}`);
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/orders.ts
import { apiClient } from './client';

export interface SupplyOrderLineCreate {
  item_id?: string | null;
  item_name: string;
  sku?: string | null;
  hsn_sac?: string | null;
  unit_id: string;
  unit_name: string;
  unit_symbol: string;
  quantity: number;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
  description?: string | null;
}

export interface SupplyOrderCreateRequest {
  order_type: 'PURCHASE' | 'SALES';
  tax_treatment: 'GST' | 'WITHOUT_GST';
  party_id: string;
  order_date: string;
  expected_date?: string | null;
  place_of_supply: string;
  lines: SupplyOrderLineCreate[];
  quotation_id?: string;
  notes?: string | null;
  terms?: string | null;
}

export interface SupplyOrderCalculateRequest {
  tax_treatment: 'GST' | 'WITHOUT_GST';
  party_id?: string | null;
  place_of_supply: string;
  lines: SupplyOrderLineCreate[];
}

export interface SupplyOrderResponse {
  id: string;
  order_type: 'PURCHASE' | 'SALES';
  tax_treatment: 'GST' | 'WITHOUT_GST';
  order_number?: string | null;
  order_date: string;
  expected_date?: string | null;
  party_id: string;
  place_of_supply: string;
  status: string;
  revision: number;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  cess_total: number;
  other_charges: number;
  round_off: number;
  grand_total: number;
  amount_in_words?: string | null;
  notes?: string | null;
  terms?: string | null;
  lines: any[];
}

export const ordersApi = {
  calculate: async (data: SupplyOrderCalculateRequest) => {
    const response = await apiClient.post<any>('/orders/calculate', data);
    return response.data;
  },
  create: async (data: SupplyOrderCreateRequest) => {
    const response = await apiClient.post<SupplyOrderResponse>('/orders', data);
    return response.data;
  },
  getAll: async (order_type?: string) => {
    const params = new URLSearchParams();
    if (order_type) params.append('order_type', order_type);
    const response = await apiClient.get<{items: SupplyOrderResponse[], total: number}>(`/orders?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<SupplyOrderResponse>(`/orders/${id}`);
    return response.data;
  },
  confirm: async (id: string) => {
    const response = await apiClient.post<SupplyOrderResponse>(`/orders/${id}/confirm`, {});
    return response.data;
  },
  convert: async (id: string) => {
    const response = await apiClient.post<any>(`/orders/${id}/convert`, {});
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/parties.ts
import { apiClient } from './client';

export interface Address {
  id?: string;
  address_type: string;
  address_line_1: string;
  address_line_2?: string;
  city: string;
  state: string;
  state_code: string;
  pincode: string;
  is_default: boolean;
}

export interface Party {
  id: string;
  party_code?: string;
  legal_name: string;
  trade_name?: string | null;
  party_type: string;
  account_type: string;
  contact_person?: string | null;
  mobile?: string | null;
  email?: string | null;
  gstin?: string | null;
  gst_registration_type?: string | null;
  pan?: string | null;
  state: string;
  state_code: string;
  place_of_supply?: string | null;
  status: string;
  addresses: Address[];
}

export interface PartyCreateRequest {
  legal_name: string;
  trade_name?: string;
  party_type: string;
  account_type: string;
  contact_person?: string;
  mobile?: string;
  email?: string;
  gstin?: string;
  gst_registration_type?: string;
  pan?: string;
  state: string;
  state_code: string;
  place_of_supply?: string;
  addresses?: Address[];
}

export const partiesApi = {
  getAll: async (account_type?: string, search?: string) => {
    const params = new URLSearchParams();
    if (account_type) params.append('account_type', account_type);
    if (search) params.append('search', search);
    const response = await apiClient.get<{items: Party[]}>(`/parties?${params.toString()}`);
    return response.data.items;
  },
  create: async (data: PartyCreateRequest) => {
    const response = await apiClient.post<Party>('/parties', data);
    return response.data;
  },
  update: async (id: string, data: Partial<PartyCreateRequest>) => {
    const response = await apiClient.put<Party>(`/parties/${id}`, data);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<Party>(`/parties/${id}`);
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/quotations.ts
import { apiClient } from './client';

export interface QuotationLineCreate {
  item_id?: string;
  item_name_snapshot: string;
  description?: string;
  hsn_sac_snapshot?: string;
  sku_snapshot?: string;
  quantity: number;
  unit_id?: string;
  unit_snapshot?: string;
  rate: number;
  discount_type?: string;
  discount_value?: number;
  gst_rate?: number;
}

export interface QuotationCreateRequest {
  quotation_type: string;
  tax_treatment: string;
  party_id: string;
  valid_until: string;
  place_of_supply: string;
  notes?: string;
  terms?: string;
  lines: QuotationLineCreate[];
}

export interface QuotationLineResponse {
  id: string;
  item_id: string | null;
  item_name_snapshot: string;
  description: string | null;
  hsn_sac_snapshot: string | null;
  sku_snapshot: string | null;
  quantity: number;
  converted_quantity: number;
  unit_id: string | null;
  unit_snapshot: string | null;
  rate: number;
  discount_type: string | null;
  discount_value: number;
  discount_amount: number;
  tax_treatment: string;
  gst_rate: number;
  taxable_value: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  cess_amount: number;
  line_total: number;
}

export interface QuotationResponse {
  id: string;
  quotation_number: string | null;
  quotation_type: string;
  tax_treatment: string;
  party_id: string;
  quotation_date: string;
  valid_until: string;
  status: string;
  revision: number;
  place_of_supply: string;
  subtotal: number;
  discount_total: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  cess_total: number;
  round_off: number;
  grand_total: number;
  notes: string | null;
  terms: string | null;
  accepted_at: string | null;
  accepted_by: string | null;
  acceptance_method: string | null;
  fully_converted: boolean;
  created_at: string;
  lines: QuotationLineResponse[];
}

export const quotationsApi = {
  create: async (data: QuotationCreateRequest) => {
    const response = await apiClient.post<QuotationResponse>('/quotations', data);
    return response.data;
  },
  getAll: async (quotationType?: string) => {
    const params = new URLSearchParams();
    if (quotationType) params.append('quotation_type', quotationType);
    const response = await apiClient.get<{items: QuotationResponse[], total: number}>(`/quotations?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<QuotationResponse>(`/quotations/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<QuotationResponse>(`/quotations/${id}/approve`, {});
    return response.data;
  },
  accept: async (id: string, acceptanceMethod: string = "USER_ACCEPTED") => {
    const response = await apiClient.post<QuotationResponse>(`/quotations/${id}/accept`, {
      acceptance_method: acceptanceMethod
    });
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/returns.ts
import { apiClient } from './client';

export interface ReturnOrderLineCreate {
  original_order_line_id: string;
  return_quantity: number;
  condition?: string;
  warehouse_action?: string;
}

export interface ReturnOrderCreateRequest {
  original_order_id: string;
  return_type: string;
  reason?: string;
  lines: ReturnOrderLineCreate[];
}

export interface ReturnOrderLineResponse {
  id: string;
  original_order_line_id: string;
  item_id: string | null;
  item_name_snapshot: string;
  unit_snapshot: string | null;
  original_quantity: number;
  previously_returned_quantity: number;
  return_quantity: number;
  remaining_quantity: number;
  rate: number;
  taxable_value: number;
  gst_rate: number;
  cgst_amount: number;
  sgst_amount: number;
  igst_amount: number;
  line_total: number;
  condition: string;
  warehouse_action: string;
}

export interface ReturnOrderResponse {
  id: string;
  return_number: string | null;
  return_type: string;
  original_order_id: string;
  party_id: string;
  return_date: string;
  status: string;
  financial_status: string;
  reason: string | null;
  subtotal: number;
  taxable_total: number;
  cgst_total: number;
  sgst_total: number;
  igst_total: number;
  grand_total: number;
  created_at: string;
  lines: ReturnOrderLineResponse[];
  settlements: any[];
}

export interface ReturnableLineResponse {
  original_order_line_id: string;
  item_name_snapshot: string;
  unit_symbol_snapshot: string | null;
  rate: number;
  gst_rate: number;
  original_quantity: number;
  previously_returned_quantity: number;
  returnable_quantity: number;
}

export interface ReturnableLinesResponse {
  order_id: string;
  order_type: string;
  tax_treatment: string;
  lines: ReturnableLineResponse[];
}

export const returnsApi = {
  getReturnableLines: async (orderId: string) => {
    const response = await apiClient.get<ReturnableLinesResponse>(`/returns/order/${orderId}/returnable-lines`);
    return response.data;
  },
  create: async (data: ReturnOrderCreateRequest) => {
    const response = await apiClient.post<ReturnOrderResponse>('/returns', data);
    return response.data;
  },
  getAll: async (returnType?: string) => {
    const params = new URLSearchParams();
    if (returnType) params.append('return_type', returnType);
    const response = await apiClient.get<{items: ReturnOrderResponse[], total: number}>(`/returns?${params.toString()}`);
    return response.data;
  },
  getById: async (id: string) => {
    const response = await apiClient.get<ReturnOrderResponse>(`/returns/${id}`);
    return response.data;
  },
  approve: async (id: string) => {
    const response = await apiClient.post<ReturnOrderResponse>(`/returns/${id}/approve`, {});
    return response.data;
  },
  post: async (id: string) => {
    const response = await apiClient.post<ReturnOrderResponse>(`/returns/${id}/post`, {});
    return response.data;
  },
  addSettlement: async (id: string, data: { settlement_type: string, amount: number, reference_number?: string, notes?: string }) => {
    const response = await apiClient.post<any>(`/returns/${id}/settlements`, data);
    return response.data;
  }
};
```

```typescript
// File: frontend/src/api/units.ts
import { apiClient } from './client';

export interface Unit {
  id: number;
  name: string;
  abbreviation: string;
  category: string;
  is_base_unit: boolean;
  base_unit_id: number | null;
  multiplier: number;
  formula: string | null;
  aliases: string | null;
}

export interface UnitCreateRequest {
  name: string;
  abbreviation: string;
  category: string;
  is_base_unit: boolean;
  base_unit_id?: number | null;
  multiplier?: number;
  formula?: string | null;
  aliases?: string | null;
}

export const unitsApi = {
  getAll: async () => {
    const response = await apiClient.get<Unit[]>('/units');
    return response.data;
  },
  create: async (data: UnitCreateRequest) => {
    const response = await apiClient.post<Unit>('/units', data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await apiClient.delete(`/units/${id}`);
    return response.data;
  }
};
```

```tsx
// File: frontend/src/app/providers.tsx
import { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

export const queryClient = new QueryClient();

// ── Auth Context ──────────────────────────────────────────────────────────────
interface AuthContextType {
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  useEffect(() => {
    const handleUnauthorized = () => logout();
    window.addEventListener('unauthorized', handleUnauthorized);
    return () => window.removeEventListener('unauthorized', handleUnauthorized);
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <AuthContext.Provider value={{ token, isAuthenticated: !!token, login, logout, isLoading: false }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};

// ── Theme Context ─────────────────────────────────────────────────────────────
type Theme = 'light' | 'dark' | 'system';

interface ThemeContextType {
  theme: Theme;
  setTheme: (t: Theme) => void;
  resolvedTheme: 'light' | 'dark';
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [theme, setThemeState] = useState<Theme>(
    () => (localStorage.getItem('theme') as Theme) || 'system'
  );
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light');

  const applyTheme = (t: Theme) => {
    const html = document.documentElement;
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const resolved = t === 'system' ? (prefersDark ? 'dark' : 'light') : t;
    setResolvedTheme(resolved);
    // shadcn uses .dark class + [data-theme] attribute
    if (resolved === 'dark') {
      html.classList.add('dark');
      html.setAttribute('data-theme', 'dark');
    } else {
      html.classList.remove('dark');
      html.setAttribute('data-theme', 'light');
    }
  };

  const setTheme = (t: Theme) => {
    localStorage.setItem('theme', t);
    setThemeState(t);
    applyTheme(t);
  };

  useEffect(() => {
    applyTheme(theme);
    const mq = window.matchMedia('(prefers-color-scheme: dark)');
    const handler = () => { if (theme === 'system') applyTheme('system'); };
    mq.addEventListener('change', handler);
    return () => mq.removeEventListener('change', handler);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error('useTheme must be used within ThemeProvider');
  return ctx;
};

// ── Combined Providers ────────────────────────────────────────────────────────
export const AppProviders = ({ children }: { children: ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AuthProvider>
          {children}
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
};
```

```tsx
// File: frontend/src/app/router.tsx
import { createBrowserRouter, Navigate, Link, useLocation } from 'react-router-dom';
import App from '../App';
import { useAuth, useTheme } from './providers';
import { lazy, Suspense } from 'react';
import { PageLoading } from '../components/common/PageLoading';

const LoginPage = lazy(() => import('../features/auth/LoginPage'));
const SetupPage = lazy(() => import('../features/auth/SetupPage'));
const PinChangePage = lazy(() => import('../features/auth/PinChangePage'));
const UnitsPage = lazy(() => import('../features/master/UnitsPage'));
const ItemsPage = lazy(() => import('../features/master/ItemsPage'));
const PartiesPage = lazy(() => import('../features/master/PartiesPage'));
const InvoiceBuilderPage = lazy(() => import('../features/invoices/InvoiceBuilderPage'));
const InvoiceListPage = lazy(() => import('../features/invoices/InvoiceListPage'));
const InvoiceDetailPage = lazy(() => import('../features/invoices/InvoiceDetailPage'));
const OrderListPage = lazy(() => import('../features/orders/OrderListPage'));
const OrderBuilderPage = lazy(() => import('../features/orders/OrderBuilderPage'));
const ReturnListPage = lazy(() => import('../features/returns/ReturnListPage'));
const ReturnBuilderPage = lazy(() => import('../features/returns/ReturnBuilderPage'));
const QuotationListPage = lazy(() => import('../features/quotations/QuotationListPage'));
const QuotationBuilderPage = lazy(() => import('../features/quotations/QuotationBuilderPage'));
const BOQListPage = lazy(() => import('../features/boqs/BOQListPage'));
const EstimateListPage = lazy(() => import('../features/estimates/EstimateListPage'));
const AdjustmentNoteListPage = lazy(() => import('../features/adjustmentNotes/AdjustmentNoteListPage'));
const AdjustmentNoteBuilderPage = lazy(() => import('../features/adjustmentNotes/AdjustmentNoteBuilderPage'));

// ── Guards ────────────────────────────────────────────────────────────────────
const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) return <Navigate to="/login" />;
  return <>{children}</>;
};

// ── Theme toggle button ───────────────────────────────────────────────────────
function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const icons = { light: '☀️', dark: '🌙', system: '💻' };
  const next: Record<string, 'dark' | 'system' | 'light'> = { light: 'dark', dark: 'system', system: 'light' };
  return (
    <button
      onClick={() => setTheme(next[theme])}
      title={`Theme: ${theme} — click to change`}
      className="text-xs px-2 py-1 rounded-md bg-muted text-muted-foreground hover:bg-accent transition-colors border border"
    >
      {icons[theme]}
    </button>
  );
}

// ── Nav link ──────────────────────────────────────────────────────────────────
function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  const loc = useLocation();
  const active = loc.pathname === to || (to !== '/' && loc.pathname.startsWith(to));
  return (
    <Link
      to={to}
      className={`block px-3 py-2 rounded-md text-sm transition-colors ${
        active ? 'bg-sidebar-accent text-sidebar-accent-foreground font-medium' : 'text-sidebar-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground'
      }`}
    >
      {children}
    </Link>
  );
}

// ── Dashboard Shell ───────────────────────────────────────────────────────────
const DashboardShell = ({ children }: { children: React.ReactNode }) => {
  const { logout } = useAuth();

  return (
    <div className="min-h-screen flex bg-background">
      {/* Sidebar */}
      <aside className="w-64 bg-sidebar border-r border-sidebar-border hidden md:flex flex-col">
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-5 border-b border-sidebar-border flex-shrink-0">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-slate-900 dark:bg-white flex items-center justify-center">
              <span className="text-white dark:text-slate-900 text-xs font-black">A</span>
            </div>
            <span className="font-black tracking-widest text-foreground text-sm uppercase">ARTHA</span>
          </Link>
          <ThemeToggle />
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-0.5">
          <NavLink to="/">Dashboard</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Sales</p>
          </div>
          <NavLink to="/invoices/new">+ Create Invoice</NavLink>
          <NavLink to="/invoices">Sales Invoices</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Purchases</p>
          </div>
          <NavLink to="/purchase-bills">Purchase Bills</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Supply</p>
          </div>
          <NavLink to="/supply-in">Supply In</NavLink>
          <NavLink to="/supply-in/quotations">↳ Quotations</NavLink>
          <NavLink to="/supply-in/returns">↳ Returns</NavLink>
          <NavLink to="/supply-out">Supply Out</NavLink>
          <NavLink to="/supply-out/quotations">↳ Quotations</NavLink>
          <NavLink to="/supply-out/returns">↳ Returns</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Documents</p>
          </div>
          <NavLink to="/boqs">BOQ</NavLink>
          <NavLink to="/estimates">Estimates</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Accounting</p>
          </div>
          <NavLink to="/credit-notes">Credit Notes</NavLink>
          <NavLink to="/debit-notes">Debit Notes</NavLink>

          <div className="pt-3 pb-1">
            <p className="px-3 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground">Master</p>
          </div>
          <NavLink to="/parties">Customers & Vendors</NavLink>
          <NavLink to="/items">Items & Products</NavLink>
          <NavLink to="/units">Units</NavLink>
        </nav>

        {/* Footer */}
        <div className="p-3 border-t border-sidebar-border space-y-1 flex-shrink-0">
          <NavLink to="/pin-change">🔐 Security PIN</NavLink>
          <button
            onClick={logout}
            className="w-full text-left block px-3 py-2 rounded-md text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            ← Logout
          </button>
        </div>
      </aside>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Mobile header */}
        <header className="h-14 bg-sidebar border-b border-sidebar-border flex items-center justify-between px-4 md:hidden">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-slate-900 dark:bg-white flex items-center justify-center">
              <span className="text-white dark:text-slate-900 text-xs font-black">A</span>
            </div>
            <span className="font-black tracking-widest text-foreground text-sm uppercase">ARTHA</span>
          </Link>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <button
              onClick={logout}
              className="text-sm text-red-500 font-medium px-3 py-1.5 rounded-md hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
            >
              Logout
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 p-4 md:p-6 overflow-auto">
          <Suspense fallback={<PageLoading />}>
            {children}
          </Suspense>
        </main>
      </div>
    </div>
  );
};

// ── Helpers for themed page elements ─────────────────────────────────────────
// Re-exported for use in page components
export { DashboardShell };

// ── Router ────────────────────────────────────────────────────────────────────
const wrap = (element: React.ReactNode) => (
  <ProtectedRoute>
    <DashboardShell>{element}</DashboardShell>
  </ProtectedRoute>
);

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: wrap(
          <div className="bg-card rounded-xl shadow-sm border border p-6">
            <h1 className="text-2xl font-bold text-foreground mb-2">Welcome to ARTHA</h1>
            <p className="text-muted-foreground mb-6">Your secure GST billing dashboard. Choose a module from the sidebar.</p>
            <div className="flex flex-wrap gap-3">
              <Link to="/invoices/new" className="px-4 py-2 bg-slate-900 dark:bg-white text-white dark:text-slate-900 rounded-lg font-medium text-sm hover:opacity-90 transition-opacity">
                Create Invoice
              </Link>
              <Link to="/invoices" className="px-4 py-2 bg-muted text-foreground rounded-lg font-medium text-sm border border hover:bg-accent transition-colors">
                View Invoices
              </Link>
            </div>
          </div>
        ),
      },
      { path: 'invoices',                  element: wrap(<InvoiceListPage />) },
      { path: 'invoices/new',              element: wrap(<InvoiceBuilderPage />) },
      { path: 'invoices/:id',              element: wrap(<InvoiceDetailPage />) },
      { path: 'purchase-bills',            element: wrap(<InvoiceListPage />) },
      { path: 'supply-in',                 element: wrap(<OrderListPage />) },
      { path: 'supply-in/quotations',      element: wrap(<QuotationListPage />) },
      { path: 'supply-in/quotations/new',  element: wrap(<QuotationBuilderPage />) },
      { path: 'supply-in/returns',         element: wrap(<ReturnListPage />) },
      { path: 'supply-in/returns/new',     element: wrap(<ReturnBuilderPage />) },
      { path: 'supply-in/new',             element: wrap(<OrderBuilderPage />) },
      { path: 'supply-out',                element: wrap(<OrderListPage />) },
      { path: 'supply-out/quotations',     element: wrap(<QuotationListPage />) },
      { path: 'supply-out/quotations/new', element: wrap(<QuotationBuilderPage />) },
      { path: 'supply-out/returns',        element: wrap(<ReturnListPage />) },
      { path: 'supply-out/returns/new',    element: wrap(<ReturnBuilderPage />) },
      { path: 'supply-out/new',            element: wrap(<OrderBuilderPage />) },
      { path: 'boqs',                      element: wrap(<BOQListPage />) },
      { path: 'estimates',                 element: wrap(<EstimateListPage />) },
      { path: 'credit-notes',              element: wrap(<AdjustmentNoteListPage noteType="CREDIT_NOTE" />) },
      { path: 'credit-notes/new',          element: wrap(<AdjustmentNoteBuilderPage noteType="CREDIT_NOTE" />) },
      { path: 'debit-notes',               element: wrap(<AdjustmentNoteListPage noteType="DEBIT_NOTE" />) },
      { path: 'debit-notes/new',           element: wrap(<AdjustmentNoteBuilderPage noteType="DEBIT_NOTE" />) },
      { path: 'parties',                   element: wrap(<PartiesPage />) },
      { path: 'items',                     element: wrap(<ItemsPage />) },
      { path: 'units',                     element: wrap(<UnitsPage />) },
      { path: 'pin-change',                element: wrap(<PinChangePage />) },
      { path: 'login',                     element: <Suspense fallback={<PageLoading />}><LoginPage /></Suspense> },
      { path: 'setup',                     element: <Suspense fallback={<PageLoading />}><SetupPage /></Suspense> },
    ],
  },
]);
```

```xml
// File: frontend/src/assets/react.svg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" aria-hidden="true" role="img" class="iconify iconify--logos" width="35.93" height="32" preserveAspectRatio="xMidYMid meet" viewBox="0 0 256 228"><path fill="#00D8FF" d="M210.483 73.824a171.49 171.49 0 0 0-8.24-2.597c.465-1.9.893-3.777 1.273-5.621c6.238-30.281 2.16-54.676-11.769-62.708c-13.355-7.7-35.196.329-57.254 19.526a171.23 171.23 0 0 0-6.375 5.848a155.866 155.866 0 0 0-4.241-3.917C100.759 3.829 77.587-4.822 63.673 3.233C50.33 10.957 46.379 33.89 51.995 62.588a170.974 170.974 0 0 0 1.892 8.48c-3.28.932-6.445 1.924-9.474 2.98C17.309 83.498 0 98.307 0 113.668c0 15.865 18.582 31.778 46.812 41.427a145.52 145.52 0 0 0 6.921 2.165a167.467 167.467 0 0 0-2.01 9.138c-5.354 28.2-1.173 50.591 12.134 58.266c13.744 7.926 36.812-.22 59.273-19.855a145.567 145.567 0 0 0 5.342-4.923a168.064 168.064 0 0 0 6.92 6.314c21.758 18.722 43.246 26.282 56.54 18.586c13.731-7.949 18.194-32.003 12.4-61.268a145.016 145.016 0 0 0-1.535-6.842c1.62-.48 3.21-.974 4.76-1.488c29.348-9.723 48.443-25.443 48.443-41.52c0-15.417-17.868-30.326-45.517-39.844Zm-6.365 70.984c-1.4.463-2.836.91-4.3 1.345c-3.24-10.257-7.612-21.163-12.963-32.432c5.106-11 9.31-21.767 12.459-31.957c2.619.758 5.16 1.557 7.61 2.4c23.69 8.156 38.14 20.213 38.14 29.504c0 9.896-15.606 22.743-40.946 31.14Zm-10.514 20.834c2.562 12.94 2.927 24.64 1.23 33.787c-1.524 8.219-4.59 13.698-8.382 15.893c-8.067 4.67-25.32-1.4-43.927-17.412a156.726 156.726 0 0 1-6.437-5.87c7.214-7.889 14.423-17.06 21.459-27.246c12.376-1.098 24.068-2.894 34.671-5.345a134.17 134.17 0 0 1 1.386 6.193ZM87.276 214.515c-7.882 2.783-14.16 2.863-17.955.675c-8.075-4.657-11.432-22.636-6.853-46.752a156.923 156.923 0 0 1 1.869-8.499c10.486 2.32 22.093 3.988 34.498 4.994c7.084 9.967 14.501 19.128 21.976 27.15a134.668 134.668 0 0 1-4.877 4.492c-9.933 8.682-19.886 14.842-28.658 17.94ZM50.35 144.747c-12.483-4.267-22.792-9.812-29.858-15.863c-6.35-5.437-9.555-10.836-9.555-15.216c0-9.322 13.897-21.212 37.076-29.293c2.813-.98 5.757-1.905 8.812-2.773c3.204 10.42 7.406 21.315 12.477 32.332c-5.137 11.18-9.399 22.249-12.634 32.792a134.718 134.718 0 0 1-6.318-1.979Zm12.378-84.26c-4.811-24.587-1.616-43.134 6.425-47.789c8.564-4.958 27.502 2.111 47.463 19.835a144.318 144.318 0 0 1 3.841 3.545c-7.438 7.987-14.787 17.08-21.808 26.988c-12.04 1.116-23.565 2.908-34.161 5.309a160.342 160.342 0 0 1-1.76-7.887Zm110.427 27.268a347.8 347.8 0 0 0-7.785-12.803c8.168 1.033 15.994 2.404 23.343 4.08c-2.206 7.072-4.956 14.465-8.193 22.045a381.151 381.151 0 0 0-7.365-13.322Zm-45.032-43.861c5.044 5.465 10.096 11.566 15.065 18.186a322.04 322.04 0 0 0-30.257-.006c4.974-6.559 10.069-12.652 15.192-18.18ZM82.802 87.83a323.167 323.167 0 0 0-7.227 13.238c-3.184-7.553-5.909-14.98-8.134-22.152c7.304-1.634 15.093-2.97 23.209-3.984a321.524 321.524 0 0 0-7.848 12.897Zm8.081 65.352c-8.385-.936-16.291-2.203-23.593-3.793c2.26-7.3 5.045-14.885 8.298-22.6a321.187 321.187 0 0 0 7.257 13.246c2.594 4.48 5.28 8.868 8.038 13.147Zm37.542 31.03c-5.184-5.592-10.354-11.779-15.403-18.433c4.902.192 9.899.29 14.978.29c5.218 0 10.376-.117 15.453-.343c-4.985 6.774-10.018 12.97-15.028 18.486Zm52.198-57.817c3.422 7.8 6.306 15.345 8.596 22.52c-7.422 1.694-15.436 3.058-23.88 4.071a382.417 382.417 0 0 0 7.859-13.026a347.403 347.403 0 0 0 7.425-13.565Zm-16.898 8.101a358.557 358.557 0 0 1-12.281 19.815a329.4 329.4 0 0 1-23.444.823c-7.967 0-15.716-.248-23.178-.732a310.202 310.202 0 0 1-12.513-19.846h.001a307.41 307.41 0 0 1-10.923-20.627a310.278 310.278 0 0 1 10.89-20.637l-.001.001a307.318 307.318 0 0 1 12.413-19.761c7.613-.576 15.42-.876 23.31-.876H128c7.926 0 15.743.303 23.354.883a329.357 329.357 0 0 1 12.335 19.695a358.489 358.489 0 0 1 11.036 20.54a329.472 329.472 0 0 1-11 20.722Zm22.56-122.124c8.572 4.944 11.906 24.881 6.52 51.026c-.344 1.668-.73 3.367-1.15 5.09c-10.622-2.452-22.155-4.275-34.23-5.408c-7.034-10.017-14.323-19.124-21.64-27.008a160.789 160.789 0 0 1 5.888-5.4c18.9-16.447 36.564-22.941 44.612-18.3ZM128 90.808c12.625 0 22.86 10.235 22.86 22.86s-10.235 22.86-22.86 22.86s-22.86-10.235-22.86-22.86s10.235-22.86 22.86-22.86Z"></path></svg>
```

```xml
// File: frontend/src/assets/vite.svg
<svg xmlns="http://www.w3.org/2000/svg" width="77" height="47" fill="none" aria-labelledby="vite-logo-title" viewBox="0 0 77 47"><title id="vite-logo-title">Vite</title><style>.parenthesis{fill:#000}@media (prefers-color-scheme:dark){.parenthesis{fill:#fff}}</style><path fill="#9135ff" d="M40.151 45.71c-.663.844-2.02.374-2.02-.699V34.708a2.26 2.26 0 0 0-2.262-2.262H24.493c-.92 0-1.457-1.04-.92-1.788l7.479-10.471c1.07-1.498 0-3.578-1.842-3.578H15.443c-.92 0-1.456-1.04-.92-1.788l9.696-13.576c.213-.297.556-.474.92-.474h28.894c.92 0 1.456 1.04.92 1.788l-7.48 10.472c-1.07 1.497 0 3.578 1.842 3.578h11.376c.944 0 1.474 1.087.89 1.83L40.153 45.712z"/><mask id="a" width="48" height="47" x="14" y="0" maskUnits="userSpaceOnUse" style="mask-type:alpha"><path fill="#000" d="M40.047 45.71c-.663.843-2.02.374-2.02-.699V34.708a2.26 2.26 0 0 0-2.262-2.262H24.389c-.92 0-1.457-1.04-.92-1.788l7.479-10.472c1.07-1.497 0-3.578-1.842-3.578H15.34c-.92 0-1.456-1.04-.92-1.788l9.696-13.575c.213-.297.556-.474.92-.474H53.93c.92 0 1.456 1.04.92 1.788L47.37 13.03c-1.07 1.498 0 3.578 1.842 3.578h11.376c.944 0 1.474 1.088.89 1.831L40.049 45.712z"/></mask><g mask="url(#a)"><g filter="url(#b)"><ellipse cx="5.508" cy="14.704" fill="#eee6ff" rx="5.508" ry="14.704" transform="rotate(269.814 20.96 11.29)scale(-1 1)"/></g><g filter="url(#c)"><ellipse cx="10.399" cy="29.851" fill="#eee6ff" rx="10.399" ry="29.851" transform="rotate(89.814 -16.902 -8.275)scale(1 -1)"/></g><g filter="url(#d)"><ellipse cx="5.508" cy="30.487" fill="#8900ff" rx="5.508" ry="30.487" transform="rotate(89.814 -19.197 -7.127)scale(1 -1)"/></g><g filter="url(#e)"><ellipse cx="5.508" cy="30.599" fill="#8900ff" rx="5.508" ry="30.599" transform="rotate(89.814 -25.928 4.177)scale(1 -1)"/></g><g filter="url(#f)"><ellipse cx="5.508" cy="30.599" fill="#8900ff" rx="5.508" ry="30.599" transform="rotate(89.814 -25.738 5.52)scale(1 -1)"/></g><g filter="url(#g)"><ellipse cx="14.072" cy="22.078" fill="#eee6ff" rx="14.072" ry="22.078" transform="rotate(93.35 31.245 55.578)scale(-1 1)"/></g><g filter="url(#h)"><ellipse cx="3.47" cy="21.501" fill="#8900ff" rx="3.47" ry="21.501" transform="rotate(89.009 35.419 55.202)scale(-1 1)"/></g><g filter="url(#i)"><ellipse cx="3.47" cy="21.501" fill="#8900ff" rx="3.47" ry="21.501" transform="rotate(89.009 35.419 55.202)scale(-1 1)"/></g><g filter="url(#j)"><ellipse cx="14.592" cy="9.743" fill="#8900ff" rx="4.407" ry="29.108" transform="rotate(39.51 14.592 9.743)"/></g><g filter="url(#k)"><ellipse cx="61.728" cy="-5.321" fill="#8900ff" rx="4.407" ry="29.108" transform="rotate(37.892 61.728 -5.32)"/></g><g filter="url(#l)"><ellipse cx="55.618" cy="7.104" fill="#00c2ff" rx="5.971" ry="9.665" transform="rotate(37.892 55.618 7.104)"/></g><g filter="url(#m)"><ellipse cx="12.326" cy="39.103" fill="#8900ff" rx="4.407" ry="29.108" transform="rotate(37.892 12.326 39.103)"/></g><g filter="url(#n)"><ellipse cx="12.326" cy="39.103" fill="#8900ff" rx="4.407" ry="29.108" transform="rotate(37.892 12.326 39.103)"/></g><g filter="url(#o)"><ellipse cx="49.857" cy="30.678" fill="#8900ff" rx="4.407" ry="29.108" transform="rotate(37.892 49.857 30.678)"/></g><g filter="url(#p)"><ellipse cx="52.623" cy="33.171" fill="#00c2ff" rx="5.971" ry="15.297" transform="rotate(37.892 52.623 33.17)"/></g></g><path d="M6.919 0c-9.198 13.166-9.252 33.575 0 46.789h6.215c-9.25-13.214-9.196-33.623 0-46.789zm62.424 0h-6.215c9.198 13.166 9.252 33.575 0 46.789h6.215c9.25-13.214 9.196-33.623 0-46.789" class="parenthesis"/><defs><filter id="b" width="60.045" height="41.654" x="-5.564" y="16.92" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="7.659"/></filter><filter id="c" width="90.34" height="51.437" x="-40.407" y="-6.762" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="7.659"/></filter><filter id="d" width="79.355" height="29.4" x="-35.435" y="2.801" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="e" width="79.579" height="29.4" x="-30.84" y="20.8" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="f" width="79.579" height="29.4" x="-29.307" y="21.949" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="g" width="74.749" height="58.852" x="29.961" y="-17.13" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="7.659"/></filter><filter id="h" width="61.377" height="25.362" x="37.754" y="3.055" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="i" width="61.377" height="25.362" x="37.754" y="3.055" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="j" width="56.045" height="63.649" x="-13.43" y="-22.082" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="k" width="54.814" height="64.646" x="34.321" y="-37.644" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="l" width="33.541" height="35.313" x="38.847" y="-10.552" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="m" width="54.814" height="64.646" x="-15.081" y="6.78" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="n" width="54.814" height="64.646" x="-15.081" y="6.78" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="o" width="54.814" height="64.646" x="22.45" y="-1.645" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter><filter id="p" width="39.409" height="43.623" x="32.919" y="11.36" color-interpolation-filters="sRGB" filterUnits="userSpaceOnUse"><feFlood flood-opacity="0" result="BackgroundImageFix"/><feBlend in="SourceGraphic" in2="BackgroundImageFix" result="shape"/><feGaussianBlur result="effect1_foregroundBlur_2002_17286" stdDeviation="4.596"/></filter></defs></svg>
```

```tsx
// File: frontend/src/components/common/Button.tsx
// Re-export from shadcn ui/ — keeps all existing import paths working
export { Button } from '../ui/button';
export type { ButtonProps } from '../ui/button';
```

```tsx
// File: frontend/src/components/common/Input.tsx
// Re-export from shadcn ui/ — keeps all existing import paths working
export { Input } from '../ui/input';
export type { InputProps } from '../ui/input';
```

```tsx
// File: frontend/src/components/common/PageLoading.tsx
export function PageLoading() {
  return (
    <div className="flex items-center justify-center p-12 text-slate-500">
      Loading...
    </div>
  );
}
```

```tsx
// File: frontend/src/components/gst/BankAccountTypeSelect.tsx
import { BANK_ACCOUNT_TYPES } from '../../lib/gst/constants';
import React from 'react';
import type { SelectHTMLAttributes } from 'react';

interface BankAccountTypeSelectProps extends SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export const BankAccountTypeSelect = React.forwardRef<
  HTMLSelectElement,
  BankAccountTypeSelectProps
>(({ label, error, className = '', id, required, ...props }, ref) => {
  const selectId = id || `bank-account-type-${Math.random().toString(36).substring(7)}`;

  return (
    <div className="w-full">
      {label && (
        <label htmlFor={selectId} className="block text-sm font-medium text-muted-foreground mb-1">
          {label}{required && <span className="text-red-500 ml-0.5">*</span>}
        </label>
      )}
      <select
        ref={ref}
        id={selectId}
        required={required}
        className={`block w-full rounded-md border shadow-sm sm:text-sm px-3 py-2 outline-none transition-colors ${
          error ? 'border-red-400 focus:border-red-500' : 'border-input focus:border-blue-500'
        } ${props.disabled ? 'bg-muted text-muted-foreground' : 'bg-card text-foreground'} ${className}`}
        {...props}
      >
        <option value="">Select Account Type</option>
        {BANK_ACCOUNT_TYPES.map((type) => (
          <option key={type.value} value={type.value}>
            {type.label}
          </option>
        ))}
      </select>
      {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
    </div>
  );
});
BankAccountTypeSelect.displayName = 'BankAccountTypeSelect';
```

```tsx
// File: frontend/src/components/gst/GSTINInput.tsx
import { useState, useCallback } from 'react';
import { validateGSTIN, parseGSTIN } from '../../lib/gst/validator';
import type { GSTINParseResult } from '../../lib/gst/validator';

interface GSTINInputProps {
  value?: string;
  onChange?: (value: string) => void;
  onValidated?: (result: GSTINParseResult | null, isValid: boolean) => void;
  name?: string;
  error?: string;
  disabled?: boolean;
  label?: string;
  showBreakdown?: boolean;
  className?: string;
}

export function GSTINInput({
  value = '',
  onChange,
  onValidated,
  name,
  error,
  disabled,
  label = 'GSTIN',
  showBreakdown = true,
  className = '',
}: GSTINInputProps) {
  const [internalValue, setInternalValue] = useState(value);

  // Sync with controlled value
  const currentValue = onChange !== undefined ? value : internalValue;

  const handleInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    // Normalize: uppercase, no spaces, only valid GSTIN chars
    const raw = e.target.value;
    const normalized = raw.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 15);
    
    if (onChange) {
      onChange(normalized);
    } else {
      setInternalValue(normalized);
    }

    if (normalized.length === 15) {
      const validation = validateGSTIN(normalized);
      if (validation.valid) {
        const parsed = parseGSTIN(normalized);
        onValidated?.(parsed, true);
      } else {
        onValidated?.(null, false);
      }
    } else {
      onValidated?.(null, false);
    }
  }, [onChange, onValidated]);

  const validation = currentValue.length > 0 ? validateGSTIN(currentValue) : null;
  const parsed = validation?.valid ? parseGSTIN(currentValue) : null;

  // Determine border color
  const borderClass = (() => {
    if (error) return 'border-red-400 focus:border-red-500 focus:ring-red-500';
    if (!validation) return 'border-input focus:border-blue-500 focus:ring-blue-500';
    if (currentValue.length === 15 && validation.valid) return 'border-green-400 focus:border-green-500 focus:ring-green-500';
    if (currentValue.length === 15 && !validation.valid) return 'border-red-400 focus:border-red-500 focus:ring-red-500';
    return 'border-input focus:border-blue-500 focus:ring-blue-500';
  })();

  return (
    <div className={`w-full ${className}`}>
      {label && (
        <label className="block text-sm font-medium text-muted-foreground mb-1">
          {label}
        </label>
      )}
      
      {/* Input */}
      <div className="relative">
        <input
          name={name}
          type="text"
          value={currentValue}
          onChange={handleInput}
          disabled={disabled}
          maxLength={15}
          placeholder="e.g. 29ABCDE1234F1Z5"
          className={`block w-full rounded-md border shadow-sm sm:text-sm px-3 py-2 outline-none font-mono tracking-wider transition-colors ${
            disabled ? 'bg-muted text-muted-foreground cursor-not-allowed' : 'bg-background'
          } ${borderClass}`}
          spellCheck={false}
          autoComplete="off"
          autoCorrect="off"
          autoCapitalize="characters"
        />
        {/* Valid checkmark */}
        {validation?.valid && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-green-500">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          </div>
        )}
        {/* Invalid X */}
        {currentValue.length === 15 && !validation?.valid && (
          <div className="absolute right-3 top-1/2 -translate-y-1/2 text-red-500">
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>

      {/* Character count + status */}
      <div className="mt-1 flex items-center justify-between">
        <div className="text-xs">
          {error ? (
            <span className="text-red-600">{error}</span>
          ) : currentValue.length === 0 ? (
            <span className="text-muted-foreground">GSTIN format: 15 characters — State Code (2) + PAN (10) + Entity (1) + Z + Check digit</span>
          ) : currentValue.length < 15 ? (
            <span className="text-muted-foreground">Enter a valid 15-character GSTIN</span>
          ) : validation?.valid ? (
            <span className="text-green-600 font-medium">✓ Valid GSTIN format</span>
          ) : (
            <span className="text-red-600">{validation?.errors[0] || '✕ Invalid GSTIN format'}</span>
          )}
        </div>
        <div className={`text-xs font-mono ${
          currentValue.length === 15 ? 'text-foreground' : 'text-muted-foreground'
        }`}>
          {currentValue.length} / 15
        </div>
      </div>

      {/* GSTIN Breakdown when valid */}
      {showBreakdown && parsed && (
        <div className="mt-2 bg-green-50 border border-green-200 rounded-md p-3">
          <div className="font-mono text-sm text-foreground flex items-center gap-1 flex-wrap">
            <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-bold">{parsed.stateCode}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-purple-100 text-purple-800 px-2 py-0.5 rounded font-bold">{parsed.pan}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-yellow-100 text-yellow-800 px-2 py-0.5 rounded font-bold">{parsed.entityNumber}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-muted text-foreground px-2 py-0.5 rounded font-bold">{parsed.defaultCharacter}</span>
            <span className="text-muted-foreground">|</span>
            <span className="bg-orange-100 text-orange-800 px-2 py-0.5 rounded font-bold">{parsed.checkDigit}</span>
          </div>
          <div className="font-mono text-xs text-muted-foreground mt-1 flex items-center gap-1 flex-wrap">
            <span className="w-[28px] text-center">State</span>
            <span className="text-transparent">|</span>
            <span className="w-[80px] text-center">PAN</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Ent</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Dflt</span>
            <span className="text-transparent">|</span>
            <span className="w-[16px] text-center">Chk</span>
          </div>
          <div className="mt-2 grid grid-cols-2 gap-x-4 gap-y-1 text-xs text-muted-foreground">
            <span><span className="font-medium">State:</span> {parsed.stateName || parsed.stateCode}</span>
            <span><span className="font-medium">PAN:</span> {parsed.pan}</span>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/components/gst/LogoUpload.tsx
import { useState, useRef } from 'react';

interface LogoUploadProps {
  currentLogoUrl?: string | null;
  onFileSelect?: (file: File) => void;
  onRemove?: () => void;
  disabled?: boolean;
  companyName?: string;
}

export function LogoUpload({ currentLogoUrl, onFileSelect, onRemove, disabled }: LogoUploadProps) {
  const [preview, setPreview] = useState<string | null>(currentLogoUrl || null);
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFile = (file: File) => {
    setError(null);
    
    // Validate type
    const allowed = ['image/png', 'image/jpeg', 'image/webp'];
    if (!allowed.includes(file.type)) {
      setError('Please upload a PNG, JPEG, or WebP image');
      return;
    }
    
    // Validate size (5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError('Image must be less than 5MB');
      return;
    }
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.onload = () => {
        if (img.width < 100 || img.height < 100) {
          setError('Image must be at least 100×100 pixels');
          return;
        }
        setPreview(e.target?.result as string);
        onFileSelect?.(file);
      };
      img.src = e.target?.result as string;
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  return (
    <div className="flex flex-col items-start gap-3">
      {/* Preview box */}
      <div
        className={`relative w-24 h-24 rounded-lg border-2 border-dashed flex items-center justify-center overflow-hidden transition-colors cursor-pointer ${
          dragOver ? 'border-blue-400 bg-blue-50' : 'border-input bg-muted hover:border-input'
        } ${disabled ? 'opacity-60 cursor-not-allowed' : ''}`}
        onClick={() => !disabled && inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        {preview ? (
          <img src={preview} alt="Company logo" className="w-full h-full object-cover" />
        ) : (
          <div className="text-center p-2">
            <svg className="w-8 h-8 text-muted-foreground mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <span className="text-xs text-muted-foreground mt-1 block">Logo</span>
          </div>
        )}
      </div>
      
      <div className="flex flex-col gap-1.5">
        <button
          type="button"
          disabled={disabled}
          onClick={() => !disabled && inputRef.current?.click()}
          className="text-sm text-blue-600 hover:text-blue-700 font-medium disabled:opacity-60 disabled:cursor-not-allowed"
        >
          {preview ? 'Change Logo' : 'Upload Logo'}
        </button>
        {preview && onRemove && (
          <button
            type="button"
            disabled={disabled}
            onClick={() => { setPreview(null); onRemove(); }}
            className="text-sm text-red-500 hover:text-red-600 disabled:opacity-60"
          >
            Remove Logo
          </button>
        )}
        <p className="text-xs text-muted-foreground">
          Square image recommended<br />
          PNG, JPEG or WebP · Min 100×100px · Max 5MB<br />
          Will be standardized to 600×600px
        </p>
      </div>
      
      {error && (
        <p className="text-sm text-red-600">{error}</p>
      )}
      
      <input
        ref={inputRef}
        type="file"
        accept="image/png,image/jpeg,image/webp"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];
          if (file) handleFile(file);
        }}
      />
    </div>
  );
}
```

```tsx
// File: frontend/src/components/gst/PhoneInput.tsx
import { useState, useRef, useEffect } from 'react';
import {
  parsePhoneNumber,
  getCountries,
  getCountryCallingCode,
  AsYouType,
  isValidPhoneNumber,
  type CountryCode,
} from 'libphonenumber-js';

// ── Country metadata ──────────────────────────────────────────────────────────
// Emoji flag from ISO 3166-1 alpha-2 code
function flagEmoji(iso: CountryCode): string {
  return iso
    .toUpperCase()
    .replace(/./g, (char) => String.fromCodePoint(char.charCodeAt(0) + 127397));
}

// Display name from browser Intl if available, fallback to code
const displayName = new Intl.DisplayNames(['en'], { type: 'region' });
function countryName(iso: CountryCode): string {
  try { return displayName.of(iso) ?? iso; } catch { return iso; }
}

// Build the full country list from libphonenumber-js at module load time
const ALL_COUNTRIES = getCountries()
  .map((iso) => ({
    iso,
    callingCode: `+${getCountryCallingCode(iso)}`,
    name: countryName(iso),
    flag: flagEmoji(iso),
  }))
  .sort((a, b) => {
    // Pin India first, then sort alphabetically
    if (a.iso === 'IN') return -1;
    if (b.iso === 'IN') return 1;
    return a.name.localeCompare(b.name);
  });

// ── Component ─────────────────────────────────────────────────────────────────
interface PhoneInputProps {
  value?: string;           // local/national number
  countryCode?: string;     // e.g. "+91"
  onValueChange?: (
    nationalNumber: string,
    callingCode: string,    // e.g. "+91"
    e164: string,           // e.g. "+919876543210"
    iso: string,            // e.g. "IN"
    isValid: boolean
  ) => void;
  label?: string;
  placeholder?: string;
  required?: boolean;
  optional?: boolean;
  error?: string;
  disabled?: boolean;
  name?: string;
  countryCodeName?: string;
}

export function PhoneInput({
  value = '',
  countryCode = '+91',
  onValueChange,
  label,
  placeholder,
  required,
  optional,
  error,
  disabled,
  name,
  countryCodeName,
}: PhoneInputProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [formatted, setFormatted] = useState(value);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);

  // Resolve the selected country from the calling code
  const selectedCountry =
    ALL_COUNTRIES.find((c) => c.callingCode === countryCode) ??
    ALL_COUNTRIES.find((c) => c.iso === 'IN')!;

  // Close dropdown on outside click
  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setSearch('');
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  // Auto-focus search when dropdown opens
  useEffect(() => {
    if (isOpen) setTimeout(() => searchRef.current?.focus(), 50);
  }, [isOpen]);

  const filtered = search
    ? ALL_COUNTRIES.filter(
        (c) =>
          c.name.toLowerCase().includes(search.toLowerCase()) ||
          c.callingCode.includes(search) ||
          c.iso.toLowerCase().includes(search.toLowerCase())
      )
    : ALL_COUNTRIES;

  const handleCountrySelect = (c: typeof ALL_COUNTRIES[number]) => {
    setIsOpen(false);
    setSearch('');
    emitChange(formatted, c.callingCode, c.iso);
  };

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value;
    // Format as you type using libphonenumber-js
    const asYouType = new AsYouType(selectedCountry.iso);
    const fmt = asYouType.input(raw);
    setFormatted(fmt);
    emitChange(fmt, selectedCountry.callingCode, selectedCountry.iso);
  };

  const emitChange = (national: string, calling: string, iso: string) => {
    if (!onValueChange) return;
    // Strip non-digits for e164 building
    const digits = national.replace(/\D/g, '');
    const e164candidate = `${calling}${digits}`;
    let e164 = e164candidate;
    let valid = false;
    try {
      const parsed = parsePhoneNumber(e164candidate, iso as CountryCode);
      if (parsed) {
        e164 = parsed.format('E.164');
        valid = parsed.isValid();
      }
    } catch {
      // partial input — leave e164 as-is, valid = false
    }
    // Fallback: also try isValidPhoneNumber
    if (!valid && digits.length >= 7) {
      try { valid = isValidPhoneNumber(e164candidate); } catch { /* noop */ }
    }
    onValueChange(national, calling, e164, iso, valid);
  };

  // Parse an incoming full e164 into national + country when value prop changes externally
  useEffect(() => {
    if (!value) return;
    if (value.startsWith('+')) {
      try {
        const parsed = parsePhoneNumber(value);
        if (parsed) setFormatted(parsed.formatNational());
      } catch { /* partial */ }
    } else {
      setFormatted(value);
    }
  }, [value]);

  const borderClass = error
    ? 'border-destructive focus-within:ring-destructive/50'
    : 'border-input focus-within:border-ring focus-within:ring-ring/30';

  return (
    <div className="w-full space-y-1">
      {label && (
        <label className="text-sm font-medium text-foreground">
          {label}
          {required && <span className="text-destructive ml-0.5">*</span>}
          {optional && <span className="text-muted-foreground font-normal ml-1">(Optional)</span>}
        </label>
      )}

      <div
        className={`flex rounded-lg border bg-background transition-all focus-within:ring-[3px] ${borderClass} ${
          disabled ? 'opacity-60 cursor-not-allowed' : ''
        }`}
      >
        {/* Country selector */}
        <div ref={dropdownRef} className="relative flex-shrink-0">
          <button
            type="button"
            disabled={disabled}
            onClick={() => setIsOpen((v) => !v)}
            className="flex items-center gap-1.5 h-9 px-3 border-r border-input rounded-l-lg text-sm font-medium text-foreground hover:bg-muted transition-colors whitespace-nowrap disabled:cursor-not-allowed"
          >
            <span className="text-base leading-none">{selectedCountry.flag}</span>
            <span className="text-muted-foreground">{selectedCountry.callingCode}</span>
            <svg className="w-3 h-3 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={isOpen ? 'M5 15l7-7 7 7' : 'M19 9l-7 7-7-7'} />
            </svg>
          </button>

          {isOpen && (
            <div className="absolute top-full left-0 z-50 mt-1 w-72 bg-popover border border-border rounded-lg shadow-lg overflow-hidden">
              {/* Search */}
              <div className="p-2 border-b border-border">
                <input
                  ref={searchRef}
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search country or code…"
                  className="w-full px-3 py-1.5 text-sm bg-background border border-input rounded-md outline-none focus:border-ring text-foreground placeholder:text-muted-foreground"
                />
              </div>
              {/* List */}
              <div className="max-h-52 overflow-y-auto">
                {filtered.length === 0 ? (
                  <p className="px-3 py-4 text-sm text-muted-foreground text-center">No results</p>
                ) : (
                  filtered.map((c) => (
                    <button
                      key={c.iso}
                      type="button"
                      onClick={() => handleCountrySelect(c)}
                      className={`w-full flex items-center gap-2.5 px-3 py-2 text-sm text-left transition-colors hover:bg-accent hover:text-accent-foreground ${
                        c.iso === selectedCountry.iso
                          ? 'bg-accent text-accent-foreground font-medium'
                          : 'text-foreground'
                      }`}
                    >
                      <span className="text-base">{c.flag}</span>
                      <span className="flex-1 truncate">{c.name}</span>
                      <span className="text-muted-foreground tabular-nums">{c.callingCode}</span>
                    </button>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* Number input */}
        <input
          name={name}
          type="tel"
          value={formatted}
          onChange={handleInput}
          disabled={disabled}
          placeholder={placeholder ?? (selectedCountry.iso === 'IN' ? '98765 43210' : 'Phone number')}
          className="flex-1 h-9 px-3 text-sm bg-transparent outline-none text-foreground placeholder:text-muted-foreground disabled:cursor-not-allowed min-w-0 rounded-r-lg"
        />
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      {/* Hidden field for form libraries that read by name */}
      {countryCodeName && (
        <input type="hidden" name={countryCodeName} value={selectedCountry.callingCode} />
      )}
    </div>
  );
}
```

```typescript
// File: frontend/src/components/gst/index.ts
export { GSTINInput } from './GSTINInput';
export { PhoneInput } from './PhoneInput';
export { LogoUpload } from './LogoUpload';
export { BankAccountTypeSelect } from './BankAccountTypeSelect';
```

```tsx
// File: frontend/src/components/invoice/InvoiceReferenceSelector.tsx
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Input } from '../ui/input';
import { Card } from '../ui/card';
import { invoicesApi, type InvoiceResponse } from '../../api/invoices';

interface Props {
  onSelect: (invoice: InvoiceResponse) => void;
  title?: string;
  transactionType?: 'SALES' | 'PURCHASE';
}

export function InvoiceReferenceSelector({ onSelect, title = "Select Source Invoice", transactionType = 'SALES' }: Props) {
  const [search, setSearch] = useState('');
  
  const { data, isLoading } = useQuery({
    queryKey: ['invoices', transactionType, search],
    queryFn: () => invoicesApi.getAll(transactionType),
  });

  const invoices = data?.items?.filter((inv: any) => 
    inv.invoice_number.toLowerCase().includes(search.toLowerCase()) ||
    inv.customer_name_snapshot.toLowerCase().includes(search.toLowerCase())
  ) || [];

  return (
    <div className="max-w-2xl mx-auto space-y-6 mt-8">
      <div>
        <h2 className="text-2xl font-bold">{title}</h2>
        <p className="text-muted-foreground">Search by Invoice Number or Customer/Supplier</p>
      </div>

      <Input 
        placeholder="Search..." 
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full text-lg p-6"
      />

      <div className="space-y-4">
        {isLoading ? (
          <p>Loading...</p>
        ) : (
          invoices.map((inv: any) => (
            <Card key={inv.id} className="p-4 hover:border-primary cursor-pointer transition-colors" onClick={() => onSelect(inv)}>
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="font-bold text-lg">{inv.invoice_number}</h3>
                  <p className="text-muted-foreground">{inv.customer_name_snapshot}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium">₹{inv.grand_total.toFixed(2)}</p>
                  <p className="text-sm text-muted-foreground">{inv.invoice_date}</p>
                </div>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
```

```tsx
// File: frontend/src/components/ui/badge.tsx
import * as React from 'react';
import { cn } from '../../lib/utils';
import { cva, type VariantProps } from 'class-variance-authority';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:     'border-transparent bg-primary text-primary-foreground',
        secondary:   'border-transparent bg-secondary text-secondary-foreground',
        destructive: 'border-transparent bg-destructive text-destructive-foreground',
        outline:     'text-foreground border-border',
        success:     'border-transparent bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        warning:     'border-transparent bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        info:        'border-transparent bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
      },
    },
    defaultVariants: { variant: 'default' },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <div className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
```

```tsx
// File: frontend/src/components/ui/button.tsx
import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '../../lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-medium transition-all disabled:pointer-events-none disabled:opacity-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 [&_svg]:pointer-events-none [&_svg:not([class*="size-"])]:size-4 shrink-0',
  {
    variants: {
      variant: {
        default:
          'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90',
        destructive:
          'bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90',
        outline:
          'border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground',
        secondary:
          'bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-9 px-4 py-2',
        sm: 'h-8 rounded-md px-3 text-xs',
        lg: 'h-10 rounded-lg px-6',
        icon: 'h-9 w-9',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  isLoading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, isLoading, children, disabled, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <svg
            className="animate-spin size-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        )}
        {children}
      </Comp>
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
```

```tsx
// File: frontend/src/components/ui/card.tsx
import * as React from 'react';
import { cn } from '../../lib/utils';

function Card({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="card"
      className={cn('bg-card text-card-foreground rounded-xl border shadow-sm', className)}
      {...props}
    />
  );
}

function CardHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="card-header"
      className={cn('flex flex-col gap-1.5 p-6', className)}
      {...props}
    />
  );
}

function CardTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      data-slot="card-title"
      className={cn('text-lg font-semibold leading-none text-card-foreground', className)}
      {...props}
    />
  );
}

function CardDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return (
    <p
      data-slot="card-description"
      className={cn('text-sm text-muted-foreground', className)}
      {...props}
    />
  );
}

function CardContent({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="card-content"
      className={cn('p-6 pt-0', className)}
      {...props}
    />
  );
}

function CardFooter({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="card-footer"
      className={cn('flex items-center p-6 pt-0', className)}
      {...props}
    />
  );
}

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
```

```tsx
// File: frontend/src/components/ui/dialog.tsx
import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '../../lib/utils';

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;
const DialogClose = DialogPrimitive.Close;

function DialogOverlay({ className, ...props }: React.ComponentProps<typeof DialogPrimitive.Overlay>) {
  return (
    <DialogPrimitive.Overlay
      data-slot="dialog-overlay"
      className={cn(
        'fixed inset-0 z-50 bg-black/60 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
        className
      )}
      {...props}
    />
  );
}

function DialogContent({ className, children, ...props }: React.ComponentProps<typeof DialogPrimitive.Content>) {
  return (
    <DialogPortal>
      <DialogOverlay />
      <DialogPrimitive.Content
        data-slot="dialog-content"
        className={cn(
          'bg-background fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 rounded-xl border p-6 shadow-xl duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]',
          className
        )}
        {...props}
      >
        {children}
        <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
          <X className="h-4 w-4" />
          <span className="sr-only">Close</span>
        </DialogPrimitive.Close>
      </DialogPrimitive.Content>
    </DialogPortal>
  );
}

function DialogHeader({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="dialog-header"
      className={cn('flex flex-col gap-2 text-center sm:text-left', className)}
      {...props}
    />
  );
}

function DialogFooter({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      data-slot="dialog-footer"
      className={cn('flex flex-col-reverse gap-2 sm:flex-row sm:justify-end', className)}
      {...props}
    />
  );
}

function DialogTitle({ className, ...props }: React.ComponentProps<typeof DialogPrimitive.Title>) {
  return (
    <DialogPrimitive.Title
      data-slot="dialog-title"
      className={cn('text-lg font-semibold leading-none text-foreground', className)}
      {...props}
    />
  );
}

function DialogDescription({ className, ...props }: React.ComponentProps<typeof DialogPrimitive.Description>) {
  return (
    <DialogPrimitive.Description
      data-slot="dialog-description"
      className={cn('text-sm text-muted-foreground', className)}
      {...props}
    />
  );
}

export {
  Dialog, DialogClose, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogOverlay, DialogPortal,
  DialogTitle, DialogTrigger,
};
```

```tsx
// File: frontend/src/components/ui/input.tsx
import * as React from 'react';
import { cn } from '../../lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: any; // accepts string | FieldError from react-hook-form
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, id, type, ...props }, ref) => {
    const inputId = id || React.useId();
    return (
      <div className="w-full space-y-1">
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium leading-none text-foreground peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
          >
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          ref={ref}
          data-slot="input"
          className={cn(
            'file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex h-9 w-full min-w-0 rounded-lg border bg-transparent px-3 py-1 text-sm shadow-sm transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50',
            error && 'border-destructive focus-visible:ring-destructive/50 focus-visible:border-destructive',
            className
          )}
          {...props}
        />
        {error && (
          <p className="text-sm text-destructive">{error}</p>
        )}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };
```

```tsx
// File: frontend/src/components/ui/label.tsx
import * as React from 'react';
import * as LabelPrimitive from '@radix-ui/react-label';
import { cn } from '../../lib/utils';

function Label({ className, ...props }: React.ComponentProps<typeof LabelPrimitive.Root>) {
  return (
    <LabelPrimitive.Root
      data-slot="label"
      className={cn(
        'flex items-center gap-2 text-sm font-medium leading-none select-none text-foreground group-data-[disabled=true]:pointer-events-none group-data-[disabled=true]:opacity-50 peer-disabled:cursor-not-allowed peer-disabled:opacity-50',
        className
      )}
      {...props}
    />
  );
}

export { Label };
```

```tsx
// File: frontend/src/components/ui/select.tsx
import * as React from 'react';
import * as SelectPrimitive from '@radix-ui/react-select';
import { Check, ChevronDown, ChevronUp } from 'lucide-react';
import { cn } from '../../lib/utils';

const Select = SelectPrimitive.Root;
const SelectGroup = SelectPrimitive.Group;
const SelectValue = SelectPrimitive.Value;

function SelectTrigger({ className, children, ...props }: React.ComponentProps<typeof SelectPrimitive.Trigger>) {
  return (
    <SelectPrimitive.Trigger
      data-slot="select-trigger"
      className={cn(
        'border-input data-[placeholder]:text-muted-foreground [&_svg:not([class*="text-"])]:text-muted-foreground focus:ring-ring/50 dark:bg-input/30 flex h-9 w-full items-center justify-between gap-2 rounded-lg border bg-transparent px-3 py-2 text-sm shadow-sm transition-[color,box-shadow] outline-none focus:ring-[3px] focus:border-ring disabled:cursor-not-allowed disabled:opacity-50 *:data-[slot=select-value]:line-clamp-1 *:data-[slot=select-value]:flex *:data-[slot=select-value]:items-center *:data-[slot=select-value]:gap-2',
        className
      )}
      {...props}
    >
      {children}
      <SelectPrimitive.Icon asChild>
        <ChevronDown className="size-4 opacity-50" />
      </SelectPrimitive.Icon>
    </SelectPrimitive.Trigger>
  );
}

function SelectScrollUpButton({ className, ...props }: React.ComponentProps<typeof SelectPrimitive.ScrollUpButton>) {
  return (
    <SelectPrimitive.ScrollUpButton
      className={cn('flex cursor-default items-center justify-center py-1', className)}
      {...props}
    >
      <ChevronUp className="size-4" />
    </SelectPrimitive.ScrollUpButton>
  );
}

function SelectScrollDownButton({ className, ...props }: React.ComponentProps<typeof SelectPrimitive.ScrollDownButton>) {
  return (
    <SelectPrimitive.ScrollDownButton
      className={cn('flex cursor-default items-center justify-center py-1', className)}
      {...props}
    >
      <ChevronDown className="size-4" />
    </SelectPrimitive.ScrollDownButton>
  );
}

function SelectContent({ className, children, position = 'popper', ...props }: React.ComponentProps<typeof SelectPrimitive.Content>) {
  return (
    <SelectPrimitive.Portal>
      <SelectPrimitive.Content
        data-slot="select-content"
        className={cn(
          'bg-popover text-popover-foreground data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 relative z-50 max-h-96 min-w-[8rem] origin-[--radix-select-content-transform-origin] overflow-hidden rounded-lg border shadow-lg',
          position === 'popper' &&
            'data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1',
          className
        )}
        position={position}
        {...props}
      >
        <SelectScrollUpButton />
        <SelectPrimitive.Viewport
          className={cn(
            'p-1',
            position === 'popper' &&
              'h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]'
          )}
        >
          {children}
        </SelectPrimitive.Viewport>
        <SelectScrollDownButton />
      </SelectPrimitive.Content>
    </SelectPrimitive.Portal>
  );
}

function SelectLabel({ className, ...props }: React.ComponentProps<typeof SelectPrimitive.Label>) {
  return (
    <SelectPrimitive.Label
      data-slot="select-label"
      className={cn('text-muted-foreground px-2 py-1.5 text-xs font-medium', className)}
      {...props}
    />
  );
}

function SelectItem({ className, children, ...props }: React.ComponentProps<typeof SelectPrimitive.Item>) {
  return (
    <SelectPrimitive.Item
      data-slot="select-item"
      className={cn(
        'focus:bg-accent focus:text-accent-foreground [&_svg:not([class*="text-"])]:text-muted-foreground relative flex w-full cursor-default select-none items-center gap-2 rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*="size-"])]:size-4',
        className
      )}
      {...props}
    >
      <span className="absolute right-2 flex size-3.5 items-center justify-center">
        <SelectPrimitive.ItemIndicator>
          <Check className="size-4" />
        </SelectPrimitive.ItemIndicator>
      </span>
      <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
    </SelectPrimitive.Item>
  );
}

function SelectSeparator({ className, ...props }: React.ComponentProps<typeof SelectPrimitive.Separator>) {
  return (
    <SelectPrimitive.Separator
      data-slot="select-separator"
      className={cn('bg-border pointer-events-none -mx-1 my-1 h-px', className)}
      {...props}
    />
  );
}

export {
  Select, SelectContent, SelectGroup, SelectItem, SelectLabel,
  SelectScrollDownButton, SelectScrollUpButton, SelectSeparator,
  SelectTrigger, SelectValue,
};
```

```tsx
// File: frontend/src/components/ui/separator.tsx
import * as React from 'react';
import * as SeparatorPrimitive from '@radix-ui/react-separator';
import { cn } from '../../lib/utils';

function Separator({ className, orientation = 'horizontal', decorative = true, ...props }: React.ComponentProps<typeof SeparatorPrimitive.Root>) {
  return (
    <SeparatorPrimitive.Root
      data-slot="separator"
      decorative={decorative}
      orientation={orientation}
      className={cn(
        'bg-border shrink-0',
        orientation === 'horizontal' ? 'h-px w-full' : 'h-full w-px',
        className
      )}
      {...props}
    />
  );
}

export { Separator };
```

```tsx
// File: frontend/src/components/ui/table.tsx
import * as React from 'react';
import { cn } from '../../lib/utils';

function Table({ className, ...props }: React.HTMLAttributes<HTMLTableElement>) {
  return (
    <div data-slot="table-container" className="relative w-full overflow-auto">
      <table
        data-slot="table"
        className={cn('w-full caption-bottom text-sm', className)}
        {...props}
      />
    </div>
  );
}

function TableHeader({ className, ...props }: React.HTMLAttributes<HTMLTableSectionElement>) {
  return (
    <thead
      data-slot="table-header"
      className={cn('bg-muted/50 [&_tr]:border-b', className)}
      {...props}
    />
  );
}

function TableBody({ className, ...props }: React.HTMLAttributes<HTMLTableSectionElement>) {
  return (
    <tbody
      data-slot="table-body"
      className={cn('[&_tr:last-child]:border-0', className)}
      {...props}
    />
  );
}

function TableFooter({ className, ...props }: React.HTMLAttributes<HTMLTableSectionElement>) {
  return (
    <tfoot
      data-slot="table-footer"
      className={cn('bg-muted/50 border-t font-medium [&>tr]:last:border-b-0', className)}
      {...props}
    />
  );
}

function TableRow({ className, ...props }: React.HTMLAttributes<HTMLTableRowElement>) {
  return (
    <tr
      data-slot="table-row"
      className={cn(
        'border-b border-border transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted',
        className
      )}
      {...props}
    />
  );
}

function TableHead({ className, ...props }: React.ThHTMLAttributes<HTMLTableCellElement>) {
  return (
    <th
      data-slot="table-head"
      className={cn(
        'text-muted-foreground h-10 px-4 text-left align-middle text-xs font-medium uppercase tracking-wider whitespace-nowrap [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]',
        className
      )}
      {...props}
    />
  );
}

function TableCell({ className, ...props }: React.TdHTMLAttributes<HTMLTableCellElement>) {
  return (
    <td
      data-slot="table-cell"
      className={cn(
        'px-4 py-3 align-middle text-sm text-foreground [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]',
        className
      )}
      {...props}
    />
  );
}

function TableCaption({ className, ...props }: React.HTMLAttributes<HTMLTableCaptionElement>) {
  return (
    <caption
      data-slot="table-caption"
      className={cn('mt-4 text-sm text-muted-foreground', className)}
      {...props}
    />
  );
}

export { Table, TableBody, TableCaption, TableCell, TableFooter, TableHead, TableHeader, TableRow };
```

```tsx
// File: frontend/src/features/adjustmentNotes/AdjustmentNoteBuilderPage.tsx
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { adjustmentNotesApi } from '../../api/adjustmentNotes';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { InvoiceReferenceSelector } from '../../components/invoice/InvoiceReferenceSelector';
import { type InvoiceResponse } from '../../api/invoices';

const schema = z.object({
  party_id: z.string().min(1, "Party is required"),
  party_role: z.enum(['CUSTOMER', 'SUPPLIER']),
  note_date: z.string().min(1, "Date is required"),
  reason_code: z.string().min(1, "Reason is required"),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  place_of_supply: z.string().min(1, "Place of supply is required"),
});

type FormData = z.infer<typeof schema>;

export default function AdjustmentNoteBuilderPage({ noteType }: { noteType: 'CREDIT_NOTE' | 'DEBIT_NOTE' }) {
  const navigate = useNavigate();
  const [sourceInvoice, setSourceInvoice] = useState<InvoiceResponse | null>(null);

  const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
    resolver: zodResolver(schema),
    values: sourceInvoice ? {
      party_id: sourceInvoice.customer_id,
      party_role: 'CUSTOMER',
      note_date: new Date().toISOString().split('T')[0],
      reason_code: 'SALES_RETURN',
      tax_treatment: sourceInvoice.tax_treatment as any,
      place_of_supply: sourceInvoice.place_of_supply || '',
    } : undefined
  });

  const createMutation = useMutation({
    mutationFn: adjustmentNotesApi.create,
    onSuccess: () => {
      navigate(`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}`);
    }
  });

  const onSubmit = (data: FormData) => {
    createMutation.mutate({
      note_type: noteType,
      ...data,
      lines: [] // Expand with a LineItem builder component
    });
  };

  if (!sourceInvoice) {
    return (
      <InvoiceReferenceSelector 
        onSelect={setSourceInvoice} 
        title={`Select Invoice for ${noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}`}
      />
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">New {noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}</h1>
        <Button variant="outline" onClick={() => setSourceInvoice(null)}>Change Invoice</Button>
      </div>

      <div className="bg-muted p-4 rounded-lg flex justify-between">
        <div>
          <p className="text-sm text-muted-foreground">Original Invoice</p>
          <p className="font-bold">{sourceInvoice.invoice_number}</p>
        </div>
        <div>
          <p className="text-sm text-muted-foreground">Customer</p>
          <p className="font-bold">{sourceInvoice.customer_name_snapshot}</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-muted-foreground">Amount</p>
          <p className="font-bold">₹{sourceInvoice.grand_total.toFixed(2)}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Party ID</label>
            <Input {...register('party_id')} disabled />
            {errors.party_id && <p className="text-red-500 text-xs mt-1">{errors.party_id.message}</p>}
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Party Role</label>
            <select {...register('party_role')} className="w-full p-2 border rounded-md" disabled>
              <option value="CUSTOMER">Customer</option>
              <option value="SUPPLIER">Supplier</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Date</label>
            <Input type="date" {...register('note_date')} />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Reason Code</label>
            <select {...register('reason_code')} className="w-full p-2 border rounded-md">
              <option value="SALES_RETURN">Sales Return</option>
              <option value="EXCESS_BILLING">Excess Billing</option>
              <option value="EXCESS_TAX">Excess Tax</option>
              <option value="POST_SALE_DISCOUNT">Post-Sale Discount</option>
              <option value="UNDER_BILLING">Under Billing</option>
              <option value="SHORT_CHARGED_TAX">Short-charged Tax</option>
              <option value="OTHER">Other</option>
            </select>
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <Button type="submit" disabled={createMutation.isPending}>
            {createMutation.isPending ? 'Saving...' : 'Create Note'}
          </Button>
        </div>
      </form>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/adjustmentNotes/AdjustmentNoteListPage.tsx
import { useQuery } from '@tanstack/react-query';
import { adjustmentNotesApi, type AdjustmentNoteResponse } from '../../api/adjustmentNotes';
import { Link } from 'react-router-dom';
import { Button } from '../../components/ui/button';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper
} from '@tanstack/react-table';

const columnHelper = createColumnHelper<AdjustmentNoteResponse>();

export default function AdjustmentNoteListPage({ noteType }: { noteType: 'CREDIT_NOTE' | 'DEBIT_NOTE' }) {
  const { data, isLoading } = useQuery({
    queryKey: ['adjustmentNotes', noteType],
    queryFn: () => adjustmentNotesApi.getAll(noteType),
  });

  const columns = [
    columnHelper.accessor('note_number', {
      header: 'Note Number',
      cell: info => info.getValue(),
    }),
    columnHelper.accessor('note_date', {
      header: 'Date',
      cell: info => new Date(info.getValue()).toLocaleDateString(),
    }),
    columnHelper.accessor('grand_total', {
      header: 'Amount',
      cell: info => `₹${info.getValue().toFixed(2)}`,
    }),
    columnHelper.accessor('status', {
      header: 'Status',
      cell: info => <span className="uppercase text-xs font-semibold">{info.getValue()}</span>,
    }),
    columnHelper.display({
      id: 'actions',
      cell: info => (
        <Link to={`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}/${info.row.original.id}`}>
          <Button variant="outline" size="sm">View</Button>
        </Link>
      )
    })
  ];

  const table = useReactTable({
    data: data?.items || [],
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          {noteType === 'CREDIT_NOTE' ? 'Credit Notes' : 'Debit Notes'}
        </h1>
        <Link to={`/${noteType === 'CREDIT_NOTE' ? 'credit-notes' : 'debit-notes'}/new`}>
          <Button>Create {noteType === 'CREDIT_NOTE' ? 'Credit Note' : 'Debit Note'}</Button>
        </Link>
      </div>

      {isLoading ? (
        <p>Loading...</p>
      ) : (
        <div className="border rounded-md">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted">
              {table.getHeaderGroups().map(headerGroup => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map(header => (
                    <th key={header.id} className="p-3 font-semibold border-b">
                      {flexRender(header.column.columnDef.header, header.getContext())}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody>
              {table.getRowModel().rows.map(row => (
                <tr key={row.id} className="border-b hover:bg-muted/50">
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id} className="p-3">
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/auth/LoginPage.tsx
import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { useAuth } from '../../app/providers';

type PinStatus = 'idle' | 'verifying' | 'success' | 'error' | 'locked';

export default function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [pin, setPin] = useState('');
  const [status, setStatus] = useState<PinStatus>('idle');
  const [errorMsg, setErrorMsg] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  // Auto-focus on mount
  useEffect(() => {
    const t = setTimeout(() => inputRef.current?.focus(), 100);
    return () => clearTimeout(t);
  }, []);

  const mutation = useMutation({
    mutationFn: authApi.login,
    onSuccess: (response) => {
      setStatus('success');
      login(response.data.token);
      navigate('/');
    },
    onError: (error: any) => {
      const msg = error.message || '';
      setPin('');
      if (msg.toLowerCase().includes('lock') || msg.toLowerCase().includes('temporarily')) {
        setStatus('locked');
        setErrorMsg(msg);
      } else {
        setStatus('error');
        setErrorMsg('Incorrect PIN');
      }
      // Re-focus so user can try again
      setTimeout(() => inputRef.current?.focus(), 80);
    },
  });

  const handlePinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
    setPin(digits);

    // Reset error when user starts typing again
    if (status === 'error' || status === 'locked') {
      setStatus('idle');
      setErrorMsg('');
    }

    // Auto-submit when 4 digits entered
    if (digits.length === 4) {
      setStatus('verifying');
      mutation.mutate({ pin: digits });
    }
  };

  const isDisabled = status === 'verifying' || status === 'locked' || status === 'success';

  const dotColor = (filled: boolean): string => {
    if (!filled) return 'bg-slate-200 dark:bg-slate-600';
    switch (status) {
      case 'success':  return 'bg-green-500 scale-110';
      case 'error':    return 'bg-red-400 scale-110 animate-bounce';
      case 'locked':   return 'bg-orange-400 scale-110';
      case 'verifying': return 'bg-blue-400 animate-pulse';
      default:          return 'bg-slate-800 dark:bg-white scale-110';
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 px-4">
      <div className="w-full max-w-sm">

        {/* Branding */}
        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-slate-900 dark:bg-white mb-4 shadow-lg">
            <span className="text-white dark:text-slate-900 text-xl font-black tracking-tighter">A</span>
          </div>
          <h1 className="text-2xl font-black tracking-widest text-slate-900 dark:text-white uppercase">ARTHA</h1>
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">Secure Billing Platform</p>
        </div>

        {/* Card */}
        <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 p-8">
          <div className="text-center mb-8">
            <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Enter your PIN</h2>
            <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">4-digit secure access code</p>
          </div>

          {/* PIN dot indicators */}
          <div className="flex justify-center gap-4 mb-4">
            {[0, 1, 2, 3].map((i) => (
              <div
                key={i}
                className={`w-4 h-4 rounded-full transition-all duration-150 ${dotColor(i < pin.length)}`}
              />
            ))}
          </div>

          {/* Hidden input — captures actual typing */}
          <input
            ref={inputRef}
            type="password"
            inputMode="numeric"
            pattern="[0-9]*"
            autoComplete="one-time-code"
            maxLength={4}
            value={pin}
            onChange={handlePinChange}
            disabled={isDisabled}
            className="sr-only"
            aria-label="Enter 4-digit PIN"
          />

          {/* Tap-target / status line */}
          <button
            type="button"
            onClick={() => !isDisabled && inputRef.current?.focus()}
            disabled={isDisabled}
            className={`w-full mt-2 py-3 rounded-xl border-2 text-sm transition-all duration-200 focus:outline-none ${
              status === 'idle' || status === 'verifying'
                ? 'border-dashed border-slate-200 dark:border-slate-600 text-slate-400 dark:text-slate-500 hover:border-slate-400 dark:hover:border-slate-400 cursor-text'
                : 'border-transparent'
            }`}
          >
            {status === 'idle' && pin.length === 0 && (
              <span>Tap here, then type your PIN</span>
            )}
            {status === 'idle' && pin.length > 0 && pin.length < 4 && (
              <span className="text-slate-500">{pin.length} of 4 digits entered…</span>
            )}
            {status === 'verifying' && (
              <span className="text-blue-500 font-medium">Verifying…</span>
            )}
            {status === 'success' && (
              <span className="text-green-600 dark:text-green-400 font-semibold">✓ PIN verified — redirecting…</span>
            )}
            {status === 'error' && (
              <span className="text-red-500 font-semibold">✕ {errorMsg}</span>
            )}
            {status === 'locked' && (
              <span className="text-orange-500 font-semibold">⚠ Account locked</span>
            )}
          </button>

          {/* Expanded error/locked message */}
          {(status === 'error' || status === 'locked') && (
            <div
              className={`mt-4 p-3 rounded-lg text-sm text-center ${
                status === 'locked'
                  ? 'bg-orange-50 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400 border border-orange-100 dark:border-orange-800'
                  : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 border border-red-100 dark:border-red-800'
              }`}
            >
              {errorMsg}
              {status === 'error' && (
                <div className="text-xs mt-1 opacity-70">Tap above and try again</div>
              )}
            </div>
          )}

          <div className="mt-6 text-center">
            <a
              href="/setup"
              className="text-xs text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors"
            >
              First time? Run setup wizard →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/auth/PinChangePage.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const pinChangeSchema = z.object({
  old_pin: z.string().length(4, 'PIN must be exactly 4 digits'),
  new_pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d+$/, 'PIN must contain only numbers'),
  confirm_pin: z.string().length(4, 'PIN must be exactly 4 digits'),
}).refine((data) => data.new_pin === data.confirm_pin, {
  message: "New PINs don't match",
  path: ["confirm_pin"],
});

type PinChangeForm = z.infer<typeof pinChangeSchema>;

export default function PinChangePage() {
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const { register, handleSubmit, formState: { errors }, reset } = useForm<PinChangeForm>({
    resolver: zodResolver(pinChangeSchema)
  });

  const mutation = useMutation({
    mutationFn: authApi.changePin,
    onSuccess: () => {
      setSuccess(true);
      reset();
      navigate('/');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to change PIN.');
    }
  });

  const onSubmit = (data: PinChangeForm) => {
    setApiError(null);
    setSuccess(false);
    mutation.mutate(data);
  };

  return (
    <div className="max-w-md mx-auto space-y-8 bg-card p-10 rounded-xl shadow border mt-12">
      <div>
        <h2 className="text-2xl font-bold text-foreground tracking-tight">
          Change Security PIN
        </h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Update your 4-digit PIN for dashboard access.
        </p>
      </div>
      
      <form className="mt-8 space-y-6" onSubmit={handleSubmit(onSubmit)}>
        {apiError && (
          <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
            {apiError}
          </div>
        )}
        {success && (
          <div className="bg-green-50 text-green-600 p-3 rounded-md text-sm border border-green-100">
            PIN changed successfully! Redirecting...
          </div>
        )}
        
        <div className="space-y-4">
          <Input
            label="Current PIN"
            type="password"
            maxLength={4}
            {...register('old_pin')}
            error={errors.old_pin?.message}
          />
          <Input
            label="New PIN"
            type="password"
            maxLength={4}
            {...register('new_pin')}
            error={errors.new_pin?.message}
          />
          <Input
            label="Confirm New PIN"
            type="password"
            maxLength={4}
            {...register('confirm_pin')}
            error={errors.confirm_pin?.message}
          />
        </div>

        <div className="flex space-x-3 pt-2">
          <Button
            type="button"
            variant="secondary"
            className="w-full"
            onClick={() => navigate('/')}
          >
            Cancel
          </Button>
          <Button
            type="submit"
            className="w-full"
            isLoading={mutation.isPending}
          >
            Update PIN
          </Button>
        </div>
      </form>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/auth/SetupPage.tsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useMutation } from '@tanstack/react-query';
import { authApi } from '../../api/auth';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { GSTINInput, PhoneInput, BankAccountTypeSelect } from '../../components/gst';

// ── Schema ────────────────────────────────────────────────────────────────────
const setupSchema = z.object({
  // Business
  company_name: z.string().min(2, 'Company name must be at least 2 characters'),
  ownership_type: z.string().min(1, 'Ownership type is required'),
  authorized_person_name: z.string().min(1, 'Authorized person name is required'),
  authorized_person_designation: z.string().optional(),
  // GST
  gst_registered: z.boolean(),
  gstin: z.string().optional(),
  tan: z.string().optional(),
  // Address
  address_line_1: z.string().min(1, 'Address is required'),
  address_line_2: z.string().optional(),
  city: z.string().min(1, 'City is required'),
  district: z.string().optional(),
  state: z.string().min(1, 'State is required'),
  state_code: z.string().min(1, 'State code is required'),
  pincode: z.string().min(4, 'Valid pincode required').max(10),
  country: z.string().default('India'),
  // Contact
  mobile: z.string().min(7, 'Mobile number required'),
  mobile_country_code: z.string().default('+91'),
  mobile_e164: z.string().optional(),
  office_phone: z.string().optional(),
  office_phone_country_code: z.string().optional(),
  office_phone_e164: z.string().optional(),
  email: z.string().email('Valid email required'),
  website: z.string().optional(),
  // Security
  pin: z.string().length(4, 'PIN must be exactly 4 digits').regex(/^\d{4}$/, 'PIN must be digits'),
  confirm_pin: z.string().length(4, 'Confirm PIN must be 4 digits'),
  // Bank — all optional
  bank_account_holder_name: z.string().optional(),
  bank_account_number: z.string().optional(),
  bank_ifsc: z.string().optional(),
  bank_name: z.string().optional(),
  bank_branch: z.string().optional(),
  bank_account_type: z.string().optional(),
}).refine(d => d.pin === d.confirm_pin, {
  message: "PINs don't match",
  path: ['confirm_pin'],
}).refine(d => {
  if (d.gst_registered && d.gstin && d.gstin.length > 0) {
    return d.gstin.length === 15;
  }
  return true;
}, { message: 'GSTIN must be exactly 15 characters', path: ['gstin'] });

type SetupForm = z.infer<typeof setupSchema>;

const OWNERSHIP_TYPES = [
  'Proprietorship', 'Partnership', 'LLP',
  'Private Limited', 'Public Limited', 'OPC',
  'HUF', 'Trust', 'Society', 'Other',
];

const TABS = [
  { id: 0, label: 'Business',  icon: '🏢' },
  { id: 1, label: 'GST & Tax', icon: '📋' },
  { id: 2, label: 'Address',   icon: '📍' },
  { id: 3, label: 'Contact',   icon: '📞' },
  { id: 4, label: 'Security',  icon: '🔐' },
  { id: 5, label: 'Bank',      icon: '🏦', optional: true },
];

// Removed CreationTransition

// ── Main wizard ───────────────────────────────────────────────────────────────
export default function SetupPage() {
  const navigate = useNavigate();
  const [tab, setTab]                 = useState(0);
  const [apiError, setApiError]       = useState<string | null>(null);
  const [gstinValid, setGstinValid]   = useState(false);
  const [skipBank, setSkipBank]       = useState(false);

  const {
    register, handleSubmit, watch, setValue, control,
    trigger, formState: { errors },
  } = useForm<any>({
    resolver: zodResolver(setupSchema),
    mode: 'onBlur',
    defaultValues: {
      gst_registered: true,
      country: 'India',
      ownership_type: 'Proprietorship',
      bank_account_type: 'CURRENT',
      mobile_country_code: '+91',
      office_phone_country_code: '+91',
    },
  });

  const mutation = useMutation({
    mutationFn: authApi.setup,
    onSuccess: () => navigate('/login'),
    onError: (error: any) => {
      setApiError(error.message || 'Setup failed. Please check your inputs.');
    },
  });

  const isGstRegistered = watch('gst_registered');
  const currentPin      = watch('pin');
  const confirmPin      = watch('confirm_pin');
  const stateValue      = watch('state');

  const pinsMatch    = currentPin?.length === 4 && confirmPin?.length === 4 && currentPin === confirmPin;
  const pinsMismatch = confirmPin?.length === 4 && currentPin !== confirmPin;

  const onSubmit = (data: SetupForm) => {
    setApiError(null);
    if (skipBank) {
      data = { ...data };
      delete (data as any).bank_account_holder_name;
      delete (data as any).bank_account_number;
      delete (data as any).bank_ifsc;
      delete (data as any).bank_name;
      delete (data as any).bank_branch;
      delete (data as any).bank_account_type;
    }
    mutation.mutate(data as any);
  };

  // Fields to validate per tab before proceeding
  const tabFields: Record<number, (keyof SetupForm)[]> = {
    0: ['company_name', 'ownership_type', 'authorized_person_name'],
    1: ['gstin'],
    2: ['address_line_1', 'city', 'state', 'state_code', 'pincode'],
    3: ['mobile', 'email'],
    4: ['pin', 'confirm_pin'],
    5: [],
  };

  const goNext = async () => {
    const valid = await trigger(tabFields[tab]);
    if (valid) setTab(t => Math.min(t + 1, TABS.length - 1));
  };

  const goBack = () => {
    setApiError(null);
    setTab(t => Math.max(t - 1, 0));
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 py-8 px-4">

        {/* ── Header / Branding ── */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-3">
            <div
              className="w-10 h-10 rounded-xl bg-slate-900 dark:bg-white flex items-center justify-center shadow-md"
              style={{ animation: 'waveFloat 3s ease-in-out infinite' }}
            >
              <span className="text-white dark:text-slate-900 text-lg font-black">A</span>
            </div>
            <span className="text-2xl font-black tracking-widest text-slate-900 dark:text-white uppercase">
              ARTHA
            </span>
          </div>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-2">Company Setup Wizard</p>
        </div>

        {/* ── Tab progress bar ── */}
        <div className="max-w-3xl mx-auto mb-6">
          <div className="flex items-center justify-center gap-1 flex-wrap">
            {TABS.map((t, i) => (
              <div key={t.id} className="flex items-center">
                <button
                  type="button"
                  onClick={() => i <= tab && setTab(i)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium transition-all duration-200 ${
                    i === tab
                      ? 'bg-slate-900 dark:bg-white text-white dark:text-slate-900 shadow-md'
                      : i < tab
                      ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 cursor-pointer'
                      : 'bg-slate-100 dark:bg-slate-700 text-slate-400 cursor-default'
                  }`}
                >
                  <span>{i < tab ? '✓' : t.icon}</span>
                  <span className="hidden sm:inline">{t.label}</span>
                  {t.optional && <span className="opacity-50 text-[10px]">(opt)</span>}
                </button>
                {i < TABS.length - 1 && (
                  <div className={`w-4 h-px mx-1 ${i < tab ? 'bg-green-400' : 'bg-slate-200 dark:bg-slate-600'}`} />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* ── Form card ── */}
        <div className="max-w-3xl mx-auto">
          <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-xl border border-slate-100 dark:border-slate-700 overflow-hidden">

            {apiError && (
              <div className="bg-red-50 dark:bg-red-900/20 border-b border-red-100 dark:border-red-800 px-6 py-3 text-sm text-red-600 dark:text-red-400">
                {apiError}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="p-6 md:p-8 min-h-[360px]">

                {/* ── TAB 0: Business ── */}
                {tab === 0 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Business Information</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">Your company's legal identity</p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <Input
                          label="Legal Company Name"
                          {...register('company_name')}
                          error={errors.company_name?.message}
                          placeholder="e.g. Acme Pvt. Ltd."
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                          Ownership Type
                        </label>
                        <select
                          {...register('ownership_type')}
                          className="block w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-700 text-slate-900 dark:text-white text-sm px-3 py-2 outline-none focus:border-slate-500 transition-colors"
                        >
                          {OWNERSHIP_TYPES.map(t => (
                            <option key={t} value={t}>{t}</option>
                          ))}
                        </select>
                      </div>
                      <Input
                        label="Authorized Person"
                        {...register('authorized_person_name')}
                        error={errors.authorized_person_name?.message}
                        placeholder="Full legal name"
                      />
                      <div className="md:col-span-2">
                        <Input
                          label="Designation (Optional)"
                          {...register('authorized_person_designation')}
                          placeholder="e.g. Director, Proprietor, Managing Partner"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* ── TAB 1: GST & Tax ── */}
                {tab === 1 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">GST & Tax Identity</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        GSTIN automatically populates State Code and PAN
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <input
                        type="checkbox"
                        id="gst_reg"
                        className="w-4 h-4 rounded border-slate-300 text-slate-900 dark:text-white"
                        {...register('gst_registered')}
                      />
                      <label htmlFor="gst_reg" className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        GST Registered
                      </label>
                    </div>

                    {isGstRegistered && (
                      <>
                        <Controller
                          name="gstin"
                          control={control}
                          render={({ field }) => (
                            <GSTINInput
                              label="GSTIN"
                              value={field.value || ''}
                              onChange={v => field.onChange(v)}
                              error={errors.gstin?.message as string}
                              onValidated={(parsed, valid) => {
                                if (valid && parsed) {
                                  setValue('state_code', parsed.stateCode, { shouldValidate: true });
                                  setValue('state', parsed.stateName || '', { shouldValidate: true });
                                  setGstinValid(true);
                                } else {
                                  setGstinValid(false);
                                }
                              }}
                            />
                          )}
                        />
                        {gstinValid && (
                          <div className="grid grid-cols-2 gap-4">
                            <Input
                              label="State Code (auto-filled)"
                              {...register('state_code')}
                              readOnly
                              className="bg-slate-50 dark:bg-slate-700 cursor-not-allowed font-mono"
                            />
                            <Input
                              label="State (auto-filled)"
                              {...register('state')}
                              readOnly
                              className="bg-slate-50 dark:bg-slate-700 cursor-not-allowed"
                            />
                          </div>
                        )}
                      </>
                    )}

                    <Input
                      label="TAN (Optional)"
                      {...register('tan')}
                      placeholder="e.g. BLRA12345B"
                    />

                    <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-3">
                      <p className="text-xs text-amber-700 dark:text-amber-300">
                        ✓ Structural GSTIN validation (15-char format + checksum). Government portal verification not performed.
                      </p>
                    </div>
                  </div>
                )}

                {/* ── TAB 2: Address ── */}
                {tab === 2 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Registered Address</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        Your company's registered office address
                      </p>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div className="md:col-span-2">
                        <Input
                          label="Address Line 1"
                          {...register('address_line_1')}
                          error={errors.address_line_1?.message}
                          placeholder="Street, Building No., Floor"
                        />
                      </div>
                      <div className="md:col-span-2">
                        <Input
                          label="Address Line 2 (Optional)"
                          {...register('address_line_2')}
                          placeholder="Area, Locality, Landmark"
                        />
                      </div>
                      <Input
                        label="City"
                        {...register('city')}
                        error={errors.city?.message}
                      />
                      <div>
                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                          District <span className="text-slate-400 font-normal text-xs">(Optional)</span>
                        </label>
                        <input
                          {...register('district')}
                          disabled={!stateValue}
                          placeholder={!stateValue ? 'Enter state first' : 'District'}
                          className={`block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors ${
                            !stateValue
                              ? 'bg-slate-50 dark:bg-slate-700/50 border-slate-200 dark:border-slate-600 text-slate-400 cursor-not-allowed'
                              : 'bg-white dark:bg-slate-700 border-slate-300 dark:border-slate-600 text-slate-900 dark:text-white focus:border-slate-500'
                          }`}
                        />
                      </div>
                      <Input
                        label="State"
                        {...register('state')}
                        error={errors.state?.message}
                        readOnly={gstinValid}
                        className={gstinValid ? 'bg-slate-50 dark:bg-slate-700 cursor-not-allowed' : ''}
                      />
                      <Input
                        label="State Code"
                        {...register('state_code')}
                        error={errors.state_code?.message}
                        readOnly={gstinValid}
                        className={gstinValid ? 'bg-slate-50 dark:bg-slate-700 cursor-not-allowed font-mono' : 'font-mono'}
                        maxLength={2}
                      />
                      <Input
                        label="Pincode"
                        {...register('pincode')}
                        error={errors.pincode?.message}
                        maxLength={10}
                        inputMode="numeric"
                      />
                      <Input
                        label="Country"
                        {...register('country')}
                        defaultValue="India"
                      />
                    </div>
                  </div>
                )}

                {/* ── TAB 3: Contact ── */}
                {tab === 3 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Contact Details</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">How customers reach your business</p>
                    </div>
                    <PhoneInput
                      label="Mobile Number"
                      required
                      value={watch('mobile') || ''}
                      countryCode={watch('mobile_country_code') || '+91'}
                      onValueChange={(phone, cc, e164, _iso) => {
                        setValue('mobile', phone);
                        setValue('mobile_country_code', cc);
                        setValue('mobile_e164', e164);
                      }}
                      error={errors.mobile?.message as string}
                    />
                    <Input
                      label="Email"
                      type="email"
                      {...register('email')}
                      error={errors.email?.message}
                      placeholder="billing@yourcompany.com"
                    />
                    <PhoneInput
                      label="Office Contact"
                      optional
                      value={watch('office_phone') || ''}
                      countryCode={watch('office_phone_country_code') || '+91'}
                      onValueChange={(phone, cc, e164, _iso) => {
                        setValue('office_phone', phone);
                        setValue('office_phone_country_code', cc);
                        setValue('office_phone_e164', e164);
                      }}
                    />
                    <Input
                      label="Website (Optional)"
                      type="url"
                      {...register('website')}
                      placeholder="https://www.yourcompany.com"
                    />
                  </div>
                )}

                {/* ── TAB 4: Security ── */}
                {tab === 4 && (
                  <div className="space-y-5">
                    <div>
                      <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Security PIN</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                        4-digit numeric PIN to access your dashboard
                      </p>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Input
                          label="Create PIN"
                          type="password"
                          inputMode="numeric"
                          maxLength={4}
                          placeholder="••••"
                          className="text-center text-2xl tracking-[0.5em]"
                          {...register('pin')}
                          error={errors.pin?.message}
                          onChange={(e) => {
                            const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
                            setValue('pin', digits, { shouldValidate: true });
                          }}
                        />
                      </div>
                      <div>
                        <Input
                          label="Confirm PIN"
                          type="password"
                          inputMode="numeric"
                          maxLength={4}
                          placeholder="••••"
                          className="text-center text-2xl tracking-[0.5em]"
                          {...register('confirm_pin')}
                          error={errors.confirm_pin?.message}
                          onChange={(e) => {
                            const digits = e.target.value.replace(/\D/g, '').slice(0, 4);
                            setValue('confirm_pin', digits, { shouldValidate: true });
                          }}
                        />
                      </div>
                    </div>

                    {pinsMatch && (
                      <div className="flex items-center gap-2 text-green-600 dark:text-green-400 text-sm">
                        <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        PINs match
                      </div>
                    )}
                    {pinsMismatch && (
                      <div className="flex items-center gap-2 text-red-500 text-sm">
                        <svg className="w-4 h-4 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                        PINs don't match
                      </div>
                    )}

                    <div className="bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 rounded-lg p-3">
                      <p className="text-xs text-slate-500 dark:text-slate-400">
                        Your PIN is hashed server-side using bcrypt. After 5 failed attempts, the account locks for 15 minutes.
                      </p>
                    </div>
                  </div>
                )}

                {/* ── TAB 5: Bank (Optional) ── */}
                {tab === 5 && (
                  <div className="space-y-5">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="text-lg font-semibold text-slate-900 dark:text-white">Bank Details</h3>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                          Optional — shown on invoices and receipts
                        </p>
                      </div>
                      <span className="text-xs bg-slate-100 dark:bg-slate-700 text-slate-500 dark:text-slate-400 px-2 py-1 rounded-full font-medium">
                        Optional
                      </span>
                    </div>

                    <div className="flex items-center gap-3 p-3 bg-slate-50 dark:bg-slate-700/50 rounded-lg border border-slate-200 dark:border-slate-600">
                      <input
                        type="checkbox"
                        id="skip_bank"
                        checked={skipBank}
                        onChange={e => setSkipBank(e.target.checked)}
                        className="w-4 h-4 rounded border-slate-300"
                      />
                      <label htmlFor="skip_bank" className="text-sm text-slate-600 dark:text-slate-300 cursor-pointer">
                        Skip bank details — I'll add them later from Settings
                      </label>
                    </div>

                    {!skipBank && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <Input
                          label="Account Holder Name"
                          {...register('bank_account_holder_name')}
                          placeholder="As per bank records"
                        />
                        <Input
                          label="Account Number"
                          {...register('bank_account_number')}
                        />
                        <Input
                          label="IFSC Code"
                          {...register('bank_ifsc')}
                          placeholder="e.g. SBIN0001234"
                          className="uppercase"
                          onChange={e => {
                            setValue('bank_ifsc', e.target.value.toUpperCase());
                          }}
                        />
                        <Input
                          label="Bank Name"
                          {...register('bank_name')}
                        />
                        <Input
                          label="Branch"
                          {...register('bank_branch')}
                        />
                        <BankAccountTypeSelect
                          label="Account Type"
                          {...register('bank_account_type')}
                        />
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* ── Footer navigation ── */}
              <div className="px-6 md:px-8 py-4 bg-slate-50 dark:bg-slate-900/50 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between gap-3">
                <div>
                  {tab > 0 && (
                    <button
                      type="button"
                      onClick={goBack}
                      className="px-4 py-2 text-sm font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white bg-white dark:bg-slate-700 border border-slate-200 dark:border-slate-600 rounded-lg transition-colors hover:shadow-sm"
                    >
                      ← Back
                    </button>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 dark:text-slate-500 tabular-nums">
                    {tab + 1} / {TABS.length}
                  </span>
                  {tab < TABS.length - 1 ? (
                    <button
                      type="button"
                      onClick={goNext}
                      className="px-5 py-2 text-sm font-semibold text-white bg-slate-900 dark:bg-white dark:text-slate-900 rounded-lg hover:bg-slate-700 dark:hover:bg-slate-100 transition-colors shadow-sm active:scale-[0.97]"
                    >
                      Continue →
                    </button>
                  ) : (
                    <Button
                      type="submit"
                      isLoading={mutation.isPending}
                      className="px-6"
                    >
                      Complete Setup
                    </Button>
                  )}
                </div>
              </div>
            </form>
          </div>
        </div>

        {/* Wave animation */}
        <style>{`
          @keyframes waveFloat {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33%       { transform: translateY(-4px) rotate(-3deg); }
            66%       { transform: translateY(2px) rotate(2deg); }
          }
        `}</style>
      </div>
    </>
  );
}
```

```tsx
// File: frontend/src/features/boqs/BOQListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { boqsApi, type BOQResponse } from '../../api/boqs';
import { Button } from '../../components/common/Button';

export default function BOQListPage() {
  const queryClient = useQueryClient();
  const [selectedBOQ, setSelectedBOQ] = useState<BOQResponse | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['boqs'],
    queryFn: boqsApi.getAll
  });

  const approveMutation = useMutation({
    mutationFn: boqsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['boqs'] });
      setSelectedBOQ(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Bills of Quantities (BOQ)</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your project BOQs and structural estimates.
          </p>
        </div>
        <Link to="/boqs/new">
          <Button>+ Create BOQ</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">BOQ No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Project Name</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={5} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading BOQs...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={5} className="px-6 py-4 text-center text-sm text-muted-foreground">No BOQs found.</td></tr>
            ) : (
              data?.items.map((b) => (
                <tr key={b.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(b.boq_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{b.boq_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{b.project_name || '-'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${b.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 'bg-blue-100 text-blue-800'}`}>
                      {b.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedBOQ(b)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {selectedBOQ && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedBOQ.boq_number || 'Draft BOQ'}
                </h3>
                <p className="text-sm text-muted-foreground">Project: {selectedBOQ.project_name} | Rev: {selectedBOQ.version}</p>
              </div>
              <button onClick={() => setSelectedBOQ(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border text-sm mb-6">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Type</th>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Description</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Est. Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Est. Amount</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedBOQ.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2 text-xs font-semibold text-muted-foreground">{line.item_type}</td>
                      <td className="px-4 py-2">
                        {line.description}
                        {line.quantity_formula && <div className="text-xs text-blue-500">Formula: {line.quantity_formula}</div>}
                      </td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_snapshot}</td>
                      <td className="px-4 py-2 text-right text-muted-foreground">₹{line.estimated_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.estimated_amount.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot className="bg-muted/50">
                  <tr>
                    <td colSpan={4} className="px-4 py-2 text-right font-bold">Total Estimated Value</td>
                    <td className="px-4 py-2 text-right font-bold text-lg">
                      ₹{selectedBOQ.lines.reduce((sum, l) => sum + l.estimated_amount, 0).toFixed(2)}
                    </td>
                  </tr>
                </tfoot>
              </table>
              {selectedBOQ.notes && (
                <div className="mt-4 p-4 bg-muted text-foreground text-sm rounded">
                  <strong>Notes:</strong> {selectedBOQ.notes}
                </div>
              )}
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedBOQ(null)}>Close</Button>
              {selectedBOQ.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedBOQ.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve BOQ
                </Button>
              )}
              {selectedBOQ.status === 'APPROVED' && (
                <Link to={`/estimates/new?boq_id=${selectedBOQ.id}`}>
                  <Button variant="default">Create Estimate</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/estimates/EstimateListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { estimatesApi, type EstimateResponse } from '../../api/estimates';
import { Button } from '../../components/common/Button';

export default function EstimateListPage() {
  const queryClient = useQueryClient();
  const [selectedEstimate, setSelectedEstimate] = useState<EstimateResponse | null>(null);

  const { data, isLoading } = useQuery({
    queryKey: ['estimates'],
    queryFn: estimatesApi.getAll
  });

  const approveMutation = useMutation({
    mutationFn: estimatesApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['estimates'] });
      setSelectedEstimate(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Cost Estimates</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Internal cost estimations and markup pricing.
          </p>
        </div>
        <Link to="/estimates/new">
          <Button>+ Create Estimate</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Estimate No</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Total Cost</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Selling Value</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={6} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading Estimates...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={6} className="px-6 py-4 text-center text-sm text-muted-foreground">No Estimates found.</td></tr>
            ) : (
              data?.items.map((e) => (
                <tr key={e.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(e.estimate_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{e.estimate_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${e.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 'bg-blue-100 text-blue-800'}`}>
                      {e.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-muted-foreground">₹{e.total_cost.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-bold text-foreground">₹{e.estimated_selling_value.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedEstimate(e)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {selectedEstimate && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-5xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedEstimate.estimate_number || 'Draft Estimate'}
                </h3>
                <p className="text-sm text-muted-foreground">Rev: {selectedEstimate.version}</p>
              </div>
              <button onClick={() => setSelectedEstimate(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border text-sm mb-6">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item Name</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-red-50">Cost Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-red-50">Cost Amt</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-blue-50">Markup %</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-blue-50">Markup Amt</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-green-50">Sell Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium bg-green-50">Sell Amt</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedEstimate.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        <div className="text-xs text-muted-foreground">{line.item_type}</div>
                      </td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_snapshot}</td>
                      <td className="px-4 py-2 text-right text-red-700 bg-red-50">₹{line.cost_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium text-red-700 bg-red-50">₹{line.cost_amount.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-blue-700 bg-blue-50">{line.markup_percent}%</td>
                      <td className="px-4 py-2 text-right text-blue-700 bg-blue-50">₹{line.markup_amount.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-green-700 bg-green-50">₹{line.selling_rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right font-medium text-green-700 bg-green-50">₹{line.selling_amount.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="grid grid-cols-2 gap-8 text-sm">
                <div className="border rounded p-4 bg-muted/50">
                  <h4 className="font-semibold mb-2">Cost Breakdown</h4>
                  <div className="flex justify-between"><span>Material</span><span>₹{selectedEstimate.material_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Labour</span><span>₹{selectedEstimate.labour_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Service</span><span>₹{selectedEstimate.service_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between"><span>Other</span><span>₹{selectedEstimate.other_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between font-bold pt-2 border-t mt-2"><span>Total Cost</span><span>₹{selectedEstimate.total_cost.toFixed(2)}</span></div>
                </div>
                
                <div className="border rounded p-4 bg-green-50">
                  <h4 className="font-semibold mb-2">Selling Breakdown</h4>
                  <div className="flex justify-between"><span>Total Cost</span><span>₹{selectedEstimate.total_cost.toFixed(2)}</span></div>
                  <div className="flex justify-between text-blue-700"><span>Total Markup</span><span>+ ₹{selectedEstimate.markup_amount.toFixed(2)}</span></div>
                  <div className="flex justify-between font-bold pt-2 border-t mt-2 text-green-800 text-lg">
                    <span>Estimated Selling Value</span>
                    <span>₹{selectedEstimate.estimated_selling_value.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedEstimate(null)}>Close</Button>
              {selectedEstimate.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedEstimate.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Estimate
                </Button>
              )}
              {selectedEstimate.status === 'APPROVED' && (
                <Link to={`/supply-out/quotations/new?estimate_id=${selectedEstimate.id}`}>
                  <Button variant="default">Create Quotation</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/invoices/InvoiceBuilderPage.tsx
import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate } from 'react-router-dom';
import { invoicesApi, type InvoiceCalculateRequest, type InvoiceCreateRequest } from '../../api/invoices';
import { itemsApi } from '../../api/items';
import { unitsApi } from '../../api/units';
import { partiesApi } from '../../api/parties';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const invoiceLineSchema = z.object({
  item_id: z.string().optional(),
  item_name: z.string().min(1, 'Item name is required'),
  description: z.string().optional(),
  hsn_sac: z.string().optional(),
  quantity: z.coerce.number().min(0.001, 'Quantity must be > 0'),
  unit_id: z.string().min(1, 'Unit is required'),
  unit_name: z.string(),
  unit_symbol: z.string(),
  rate: z.coerce.number().min(0),
  discount_type: z.string().default('NONE'),
  discount_value: z.coerce.number().default(0),
  gst_rate: z.coerce.number().default(0),
});

const invoiceSchema = z.object({
  invoice_type: z.string().default('TAX_INVOICE'),
  invoice_date: z.string().min(1, 'Date is required'),
  customer_id: z.string().min(1, 'Customer is required'),
  place_of_supply: z.string().min(1, 'Place of supply is required'),
  lines: z.array(invoiceLineSchema).min(1, 'At least one line is required'),
  notes: z.string().optional(),
  terms: z.string().optional(),
});

export default function InvoiceBuilderPage() {
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: items = [] } = useQuery({ queryKey: ['items'], queryFn: itemsApi.getAll });
  const { data: units = [] } = useQuery({ queryKey: ['units'], queryFn: unitsApi.getAll });
  const { data: parties = [] } = useQuery({ queryKey: ['parties'], queryFn: () => partiesApi.getAll() });

  const { register, control, handleSubmit, watch, setValue, formState: { errors } } = useForm<any>({
    resolver: zodResolver(invoiceSchema),
    defaultValues: {
      invoice_type: 'TAX_INVOICE',
      invoice_date: new Date().toISOString().split('T')[0],
      place_of_supply: '',
      lines: [{ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0 }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const watchAll = watch();

  const calculateMutation = useMutation({
    mutationFn: invoicesApi.calculate,
  });

  const createMutation = useMutation({
    mutationFn: invoicesApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      alert(`Invoice Draft Created! Draft ID: ${data.id}`);
      navigate('/');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create invoice');
    }
  });

  // Debounced calculate
  useEffect(() => {
    if (!watchAll.lines || watchAll.lines.length === 0) return;
    
    // Quick validation before hitting backend
    const isValidForCalc = watchAll.lines.every((l: any) => l.item_name && l.quantity > 0 && l.unit_id);
    if (!isValidForCalc) return;

    const timeoutId = setTimeout(() => {
      const calcData: InvoiceCalculateRequest = {
        customer_id: watchAll.customer_id || null,
        place_of_supply: watchAll.place_of_supply || '29', // Default state code fallback
        lines: watchAll.lines.map((l: any) => ({
          item_id: l.item_id,
          item_name: l.item_name,
          description: l.description,
          hsn_sac: l.hsn_sac,
          quantity: Number(l.quantity) || 0,
          unit_id: l.unit_id,
          unit_name: l.unit_name || 'Unit',
          unit_symbol: l.unit_symbol || 'U',
          rate: Number(l.rate) || 0,
          discount_type: l.discount_type,
          discount_value: Number(l.discount_value) || 0,
          gst_rate: Number(l.gst_rate) || 0,
        }))
      };
      
      calculateMutation.mutate(calcData);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [JSON.stringify(watchAll.lines), watchAll.customer_id, watchAll.place_of_supply]);

  const handleItemSelect = (index: number, itemId: string) => {
    const item = items.find((i: any) => i.id.toString() === itemId);
    if (item) {
      setValue(`lines.${index}.item_id`, item.id.toString());
      setValue(`lines.${index}.item_name`, item.name);
      setValue(`lines.${index}.description`, item.description || '');
      setValue(`lines.${index}.hsn_sac`, item.hsn_sac || '');
      setValue(`lines.${index}.rate`, item.sale_price);
      setValue(`lines.${index}.gst_rate`, item.gst_rate);
      
      const unit = units.find((u: any) => u.id === item.unit_id);
      if (unit) {
        setValue(`lines.${index}.unit_id`, unit.id.toString());
        setValue(`lines.${index}.unit_name`, unit.name);
        setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
      }
    }
  };

  const handleCustomerSelect = (customerId: string) => {
    const customer = parties.find((p: any) => p.id === customerId);
    if (customer) {
      setValue('place_of_supply', customer.state_code);
    }
  };

  const handleUnitSelect = (index: number, unitId: string) => {
    const unit = units.find((u: any) => u.id.toString() === unitId);
    if (unit) {
      setValue(`lines.${index}.unit_id`, unit.id.toString());
      setValue(`lines.${index}.unit_name`, unit.name);
      setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
    }
  };

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate(data as InvoiceCreateRequest);
  };

  const calcData = calculateMutation.data;

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-20">
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Create Tax Invoice</h2>
          <p className="mt-1 text-sm text-muted-foreground">Generate a new GST compliant invoice.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {apiError && (
          <div className="bg-red-50 text-red-600 p-4 rounded-md text-sm border border-red-100 font-medium">
            Error: {apiError}
          </div>
        )}

        {/* Header Information */}
        <div className="bg-card p-6 rounded-lg shadow-sm border grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <label className="block text-sm font-medium text-muted-foreground mb-1">Customer</label>
            <select 
              className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500"
              {...register('customer_id')}
              onChange={(e) => {
                register('customer_id').onChange(e);
                handleCustomerSelect(e.target.value);
              }}
            >
              <option value="">Select Customer...</option>
              {parties.map((p: any) => (
                <option key={p.id} value={p.id}>{p.legal_name} {p.gstin ? `(${p.gstin})` : ''}</option>
              ))}
            </select>
            {errors.customer_id?.message && <p className="mt-1 text-sm text-red-600">{errors.customer_id.message as string}</p>}
          </div>

          <Input label="Invoice Date" type="date" {...register('invoice_date')} error={errors.invoice_date?.message} />
          <Input label="Place of Supply (State Code)" {...register('place_of_supply')} error={errors.place_of_supply?.message} placeholder="e.g. 29" />
        </div>

        {/* Invoice Lines */}
        <div className="bg-card p-6 rounded-lg shadow-sm border space-y-4">
          <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Items & Services</h3>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-border text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-1/4">Item / Product</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-24">HSN</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Qty</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-28">Unit</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-28">Rate (₹)</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Discount</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-20">GST %</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-32">Amount</th>
                  <th className="px-3 py-2 w-10"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {fields.map((field, index) => {
                  const calculatedLine = calcData?.lines?.[index];
                  return (
                    <tr key={field.id} className="hover:bg-muted/50">
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1 mb-1"
                          onChange={(e) => handleItemSelect(index, e.target.value)}
                        >
                          <option value="">Select Item...</option>
                          {items.map((i: any) => (
                            <option key={i.id} value={i.id}>{i.name}</option>
                          ))}
                        </select>
                        <input type="text" placeholder="Item Name" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.item_name`)} />
                      </td>
                      <td className="px-3 py-2">
                        <input type="text" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.hsn_sac`)} />
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.quantity`)} />
                      </td>
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1"
                          {...register(`lines.${index}.unit_id`)}
                          onChange={(e) => {
                            register(`lines.${index}.unit_id`).onChange(e);
                            handleUnitSelect(index, e.target.value);
                          }}
                        >
                          <option value="">Unit...</option>
                          {units.map((u: any) => (
                            <option key={u.id} value={u.id}>{u.abbreviation}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.rate`)} />
                      </td>
                      <td className="px-3 py-2">
                        <div className="flex space-x-1">
                          <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.discount_value`)} />
                          <select className="block rounded border-input shadow-sm text-xs border px-1 py-1 bg-muted/50" {...register(`lines.${index}.discount_type`)}>
                            <option value="NONE">None</option>
                            <option value="PERCENT">%</option>
                            <option value="FIXED">₹</option>
                          </select>
                        </div>
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.gst_rate`)} />
                      </td>
                      <td className="px-3 py-2 text-right font-medium text-foreground bg-muted/50">
                        {calculateMutation.isPending ? '...' : (calculatedLine?.line_total ? `₹${calculatedLine.line_total.toFixed(2)}` : '₹0.00')}
                      </td>
                      <td className="px-3 py-2 text-center">
                        <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 font-bold p-1">×</button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          
          <Button 
            type="button" 
            variant="secondary" 
            onClick={() => append({ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0 })}
          >
            + Add Line
          </Button>
        </div>

        {/* Totals & Notes */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Customer Notes</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('notes')} />
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Terms & Conditions</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('terms')} />
            </div>
          </div>

          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Invoice Summary</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-muted-foreground">
                <span>Subtotal</span>
                <span>₹{(calcData?.subtotal || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-red-600">
                <span>Discount</span>
                <span>- ₹{(calcData?.discount_total || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-foreground font-medium pt-2 border-t">
                <span>Taxable Value</span>
                <span>₹{(calcData?.taxable_total || 0).toFixed(2)}</span>
              </div>
              
              {(calcData?.igst_total || 0) > 0 ? (
                <div className="flex justify-between text-muted-foreground">
                  <span>IGST</span>
                  <span>₹{(calcData?.igst_total || 0).toFixed(2)}</span>
                </div>
              ) : (
                <>
                  <div className="flex justify-between text-muted-foreground">
                    <span>CGST</span>
                    <span>₹{(calcData?.cgst_total || 0).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-muted-foreground">
                    <span>SGST / UTGST</span>
                    <span>₹{(calcData?.sgst_total || 0).toFixed(2)}</span>
                  </div>
                </>
              )}

              <div className="flex justify-between text-xl font-bold text-foreground pt-4 border-t mt-4">
                <span>Grand Total</span>
                <span>₹{(calcData?.grand_total || 0).toFixed(2)}</span>
              </div>

              {calcData?.amount_in_words && (
                <div className="text-xs text-muted-foreground text-right italic mt-1">
                  Rupees {calcData.amount_in_words}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="fixed bottom-0 left-0 right-0 bg-card border-t p-4 shadow-lg flex justify-end space-x-4 z-10 md:ml-64">
          <Button type="button" variant="secondary" onClick={() => navigate('/')}>Cancel</Button>
          <Button type="submit" isLoading={createMutation.isPending} disabled={calculateMutation.isPending || !calcData?.grand_total}>
            Save Draft Invoice
          </Button>
        </div>
      </form>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/invoices/InvoiceDetailPage.tsx
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { invoicesApi } from '../../api/invoices';
import { Button } from '../../components/ui/button';

export default function InvoiceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState('overview');

  const { data: invoice, isLoading } = useQuery({
    queryKey: ['invoice', id],
    queryFn: async () => {
      // Replace with a dedicated GET endpoint for a single invoice in the future.
      const res = await invoicesApi.getAll('SALES');
      return res.items.find((i: any) => i.id === id) || null;
    }
  });

  if (isLoading) return <div>Loading...</div>;
  if (!invoice) return <div>Invoice not found.</div>;

  const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'items', label: 'Items' },
    { id: 'payments', label: 'Payments' },
    { id: 'returns', label: 'Returns' },
    { id: 'credit_notes', label: 'Credit Notes' },
    { id: 'debit_notes', label: 'Debit Notes' },
    { id: 'documents', label: 'Documents' },
    { id: 'timeline', label: 'Timeline' },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6 mt-4">
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-3xl font-bold">{invoice.invoice_number}</h1>
            <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-bold">
              {invoice.invoice_status}
            </span>
          </div>
          <p className="text-muted-foreground mt-1">{invoice.customer_name_snapshot} • {invoice.invoice_date}</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline">Payment</Button>
          <Button variant="outline">Credit Note</Button>
          <Button variant="outline" onClick={() => invoicesApi.getPdf(invoice.id)}>Download PDF</Button>
        </div>
      </div>

      <div className="border-b">
        <nav className="flex space-x-8 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors
                ${activeTab === tab.id 
                  ? 'border-primary text-primary' 
                  : 'border-transparent text-muted-foreground hover:text-foreground hover:border-muted'
                }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      <div className="pt-4">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-3 gap-6">
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Invoice Amount</p>
              <p className="text-2xl font-bold">₹{invoice.grand_total.toFixed(2)}</p>
            </div>
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Outstanding</p>
              <p className="text-2xl font-bold text-red-500">₹{invoice.grand_total.toFixed(2)}</p>
            </div>
            <div className="bg-card border p-4 rounded-lg">
              <p className="text-sm text-muted-foreground mb-1">Status</p>
              <p className="text-xl font-medium">{invoice.payment_status || 'UNPAID'}</p>
            </div>
          </div>
        )}

        {activeTab === 'documents' && (
          <div className="p-6 bg-card border rounded-lg">
            <h3 className="font-bold mb-6">DOCUMENT HISTORY</h3>
            <div className="flex flex-col items-center space-y-4">
              <div className="w-64 p-4 border rounded shadow-sm text-center">
                <p className="text-xs text-muted-foreground font-bold uppercase">Supply Out</p>
                <p className="font-medium">SO-000083</p>
              </div>
              <div className="h-6 w-px bg-border"></div>
              <div className="w-64 p-4 border-2 border-primary rounded shadow-md text-center bg-primary/5">
                <p className="text-xs text-primary font-bold uppercase">Invoice</p>
                <p className="font-bold">{invoice.invoice_number}</p>
              </div>
              <div className="h-6 w-px bg-border"></div>
              <div className="grid grid-cols-2 gap-8 relative">
                <div className="w-48 p-4 border rounded shadow-sm text-center">
                  <p className="text-xs text-muted-foreground font-bold uppercase">Payment</p>
                  <p className="font-medium text-green-600">PAY-000315</p>
                </div>
                <div className="w-48 p-4 border rounded shadow-sm text-center">
                  <p className="text-xs text-muted-foreground font-bold uppercase">Credit Note</p>
                  <p className="font-medium text-orange-600">CN-000025</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'timeline' && (
          <div className="space-y-4">
             <div className="flex gap-4">
               <div className="w-24 text-sm text-muted-foreground mt-1">Today 10:00</div>
               <div className="border-l-2 pl-4 pb-6 border-border">
                 <p className="font-medium">Invoice Finalized</p>
                 <p className="text-sm text-muted-foreground">Invoice number {invoice.invoice_number} was assigned.</p>
               </div>
             </div>
             <div className="flex gap-4">
               <div className="w-24 text-sm text-muted-foreground mt-1">Yesterday</div>
               <div className="border-l-2 pl-4 pb-6 border-transparent">
                 <p className="font-medium">Invoice Draft Created</p>
                 <p className="text-sm text-muted-foreground">Draft was created.</p>
               </div>
             </div>
          </div>
        )}
      </div>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/invoices/InvoiceListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { invoicesApi, type InvoiceResponse } from '../../api/invoices';
import { Button } from '../../components/common/Button';

export default function InvoiceListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedInvoice, setSelectedInvoice] = useState<InvoiceResponse | null>(null);
  
  const isPurchase = location.pathname.includes('purchase-bills');
  const transactionType = isPurchase ? 'PURCHASE' : 'SALES';
  const pageTitle = isPurchase ? 'Purchase Bills' : 'Sales Invoices';
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['invoices', transactionType],
    queryFn: () => invoicesApi.getAll(transactionType)
  });
  
  const invoices = data?.items || [];

  const finalizeMutation = useMutation({
    mutationFn: invoicesApi.finalize,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setSelectedInvoice(null);
    }
  });

  const cancelMutation = useMutation({
    mutationFn: ({ id, reason }: { id: string, reason: string }) => invoicesApi.cancel(id, reason),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      setSelectedInvoice(null);
    }
  });

  const handleFinalize = (id: string) => {
    if (confirm('Are you sure you want to finalize this invoice? Once finalized, it will be locked and an Invoice Number will be generated.')) {
      finalizeMutation.mutate(id);
    }
  };

  const handleCancel = (id: string) => {
    const reason = prompt('Please enter a reason for cancelling this invoice:');
    if (reason && reason.length >= 5) {
      cancelMutation.mutate({ id, reason });
    } else if (reason !== null) {
      alert('Cancellation reason must be at least 5 characters long.');
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage your {pageTitle.toLowerCase()}.</p>
        </div>
        {!isPurchase && (
          <Link to="/invoices/new" className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 font-medium text-sm">
            + Create Invoice
          </Link>
        )}
      </div>

      {isLoading ? (
        <div>Loading invoices...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{isPurchase ? 'Bill #' : 'Invoice #'}</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
                <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {invoices.map((inv) => (
                <tr key={inv.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">
                    {inv.invoice_number.startsWith('DRAFT-') ? <span className="text-gray-400 italic">DRAFT</span> : inv.invoice_number}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{inv.invoice_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{inv.customer_name_snapshot}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-right text-foreground">₹{inv.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${inv.invoice_status === 'DRAFT' ? 'bg-yellow-100 text-yellow-800' : 
                        inv.invoice_status === 'FINALIZED' ? 'bg-green-100 text-green-800' : 
                        'bg-red-100 text-red-800'}`}>
                      {inv.invoice_status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => setSelectedInvoice(inv)}
                      className="text-primary-600 hover:text-primary-900"
                    >
                      View
                    </button>
                  </td>
                </tr>
              ))}
              {invoices.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-6 py-8 text-center text-muted-foreground">
                    No invoices found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {/* View Modal */}
      {selectedInvoice && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setSelectedInvoice(null)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
              
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-xl font-bold text-foreground">
                    {selectedInvoice.invoice_status === 'DRAFT' ? 'Draft Invoice' : `Tax Invoice: ${selectedInvoice.invoice_number}`}
                  </h3>
                  <p className="text-sm text-muted-foreground">Date: {selectedInvoice.invoice_date}</p>
                </div>
                <div className={`px-3 py-1 rounded text-sm font-bold 
                  ${selectedInvoice.invoice_status === 'FINALIZED' ? 'bg-green-100 text-green-800' : 
                    selectedInvoice.invoice_status === 'CANCELLED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'}`}>
                  {selectedInvoice.invoice_status}
                </div>
              </div>

              <div className="border rounded-md p-4 mb-6 bg-muted/50">
                <h4 className="text-sm font-semibold text-muted-foreground mb-2">{isPurchase ? 'From Supplier:' : 'Billed To:'}</h4>
                <p className="font-medium text-foreground">{selectedInvoice.customer_name_snapshot}</p>
                <p className="text-sm text-muted-foreground">Place of Supply: {selectedInvoice.place_of_supply}</p>
              </div>

              <div className="overflow-x-auto mb-6">
                <table className="min-w-full text-sm">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-3 py-2 text-left">Item</th>
                      <th className="px-3 py-2 text-right">Qty</th>
                      <th className="px-3 py-2 text-right">Rate</th>
                      <th className="px-3 py-2 text-right">GST %</th>
                      <th className="px-3 py-2 text-right">Total</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {selectedInvoice.lines.map((line: any) => (
                      <tr key={line.id}>
                        <td className="px-3 py-2">{line.item_name}</td>
                        <td className="px-3 py-2 text-right">{line.quantity} {line.unit_symbol_snapshot}</td>
                        <td className="px-3 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                        <td className="px-3 py-2 text-right">{line.gst_rate}%</td>
                        <td className="px-3 py-2 text-right">₹{line.line_total.toFixed(2)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="flex justify-end mb-6">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal:</span>
                    <span className="font-medium">₹{selectedInvoice.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Taxable Value:</span>
                    <span className="font-medium">₹{selectedInvoice.taxable_total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg border-t pt-2 mt-2">
                    <span>Grand Total:</span>
                    <span>₹{selectedInvoice.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              <div className="pt-4 border-t flex justify-end space-x-3">
                <Button type="button" variant="secondary" onClick={() => setSelectedInvoice(null)}>Close</Button>
                
                <Button 
                  type="button" 
                  variant="secondary"
                  onClick={() => invoicesApi.getPdf(selectedInvoice.id)}
                >
                  View PDF
                </Button>

                {selectedInvoice.invoice_status === 'FINALIZED' && (
                  <Button 
                    type="button" 
                    variant="destructive" 
                    onClick={() => handleCancel(selectedInvoice.id)}
                    isLoading={cancelMutation.isPending}
                  >
                    Cancel Invoice
                  </Button>
                )}

                {selectedInvoice.invoice_status === 'DRAFT' && (
                  <Button 
                    type="button" 
                    onClick={() => handleFinalize(selectedInvoice.id)}
                    isLoading={finalizeMutation.isPending}
                  >
                    Finalize & Generate Number
                  </Button>
                )}
              </div>

            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/master/ItemsPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { itemsApi } from '../../api/items';
import { unitsApi } from '../../api/units';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const itemSchema = z.object({
  type: z.string().min(1, 'Type is required'),
  name: z.string().min(1, 'Name is required'),
  sku: z.string().optional(),
  description: z.string().optional(),
  hsn_sac: z.string().optional(),
  gst_rate: z.coerce.number().min(0).max(100),
  cess_rate: z.coerce.number().min(0).max(100).optional(),
  sale_price: z.coerce.number().min(0),
  purchase_price: z.coerce.number().min(0),
  unit_id: z.string().min(1, 'Unit is required'),
  stock_quantity: z.coerce.number().optional(),
  low_stock_warning: z.coerce.number().optional(),
});

type ItemForm = z.infer<typeof itemSchema>;

export default function ItemsPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: items = [], isLoading: itemsLoading } = useQuery({
    queryKey: ['items'],
    queryFn: itemsApi.getAll
  });

  const { data: units = [] } = useQuery({
    queryKey: ['units'],
    queryFn: unitsApi.getAll
  });

  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm<any>({
    resolver: zodResolver(itemSchema),
    defaultValues: {
      type: 'Product',
      gst_rate: 18,
      cess_rate: 0,
      sale_price: 0,
      purchase_price: 0,
      stock_quantity: 0,
      low_stock_warning: 0
    }
  });

  const itemType = watch('type');

  const createMutation = useMutation({
    mutationFn: itemsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
      setIsModalOpen(false);
      reset();
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create item');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: itemsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['items'] });
    }
  });

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate({
      ...(data as ItemForm),
      unit_id: parseInt(data.unit_id),
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Products & Services</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage your inventory, pricing, and HSN/SAC codes.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)}>Add New Item</Button>
      </div>

      {itemsLoading ? (
        <div>Loading items...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Item Name / SKU</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type & HSN</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Sale Price</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Stock</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {items.map((item) => (
                <tr key={item.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-foreground">{item.name}</div>
                    <div className="text-xs text-muted-foreground">{item.sku || 'No SKU'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${item.type === 'Service' ? 'bg-purple-100 text-purple-800' : 'bg-blue-100 text-blue-800'}`}>
                      {item.type}
                    </span>
                    <div className="text-xs text-muted-foreground mt-1">{item.hsn_sac ? `HSN: ${item.hsn_sac}` : '-'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm text-foreground font-medium">
                    ₹{item.sale_price.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm">
                    {item.type === 'Product' ? (
                      <span className={item.stock_quantity <= item.low_stock_warning ? 'text-red-600 font-semibold' : 'text-green-600 font-semibold'}>
                        {item.stock_quantity}
                      </span>
                    ) : (
                      <span className="text-gray-400">N/A</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this item?')) {
                          deleteMutation.mutate(item.id);
                        }
                      }}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">
                    No items found. Click "Add New Item" to create one.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setIsModalOpen(false)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4 border-b pb-2">Add New Item</h3>
              
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Basic Details */}
                  <div className="space-y-4 md:col-span-2 grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Item Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('type')}>
                        <option value="Product">Product (Goods)</option>
                        <option value="Service">Service</option>
                      </select>
                    </div>
                    <Input label="Name" {...register('name')} error={errors.name?.message} />
                  </div>

                  <Input label="SKU / Item Code" {...register('sku')} error={errors.sku?.message} />
                  <Input label="HSN/SAC Code" {...register('hsn_sac')} error={errors.hsn_sac?.message} />
                  
                  <div className="md:col-span-2">
                    <Input label="Description (Optional)" {...register('description')} error={errors.description?.message} />
                  </div>

                  {/* Pricing Details */}
                  <div className="md:col-span-2 bg-muted p-4 rounded-md border border">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Pricing & Tax</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <Input label="Sale Price" type="number" step="0.01" {...register('sale_price')} error={errors.sale_price?.message} />
                      <Input label="Purchase Price" type="number" step="0.01" {...register('purchase_price')} error={errors.purchase_price?.message} />
                      <Input label="GST Rate (%)" type="number" step="0.1" {...register('gst_rate')} error={errors.gst_rate?.message} />
                      <Input label="CESS Rate (%)" type="number" step="0.1" {...register('cess_rate')} error={errors.cess_rate?.message} />
                    </div>
                  </div>

                  {/* Inventory Details */}
                  <div className="md:col-span-2">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-muted-foreground mb-1">Primary Unit</label>
                        <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('unit_id')}>
                          <option value="">Select a unit...</option>
                          {units.map(u => (
                            <option key={u.id} value={u.id}>{u.name} ({u.abbreviation})</option>
                          ))}
                        </select>
                        {errors.unit_id?.message && <p className="mt-1 text-sm text-red-600">{errors.unit_id.message as string}</p>}
                      </div>
                      
                      {itemType === 'Product' && (
                        <div className="grid grid-cols-2 gap-4">
                          <Input label="Opening Stock" type="number" step="any" {...register('stock_quantity')} error={errors.stock_quantity?.message} />
                          <Input label="Low Stock Warning" type="number" step="any" {...register('low_stock_warning')} error={errors.low_stock_warning?.message} />
                        </div>
                      )}
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Item</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/master/PartiesPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { partiesApi } from '../../api/parties';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { GSTINInput, PhoneInput, BankAccountTypeSelect } from '../../components/gst';

const partySchema = z.object({
  legal_name: z.string().min(1, 'Legal name is required'),
  trade_name: z.string().optional(),
  party_type: z.string().min(1, 'Party type is required'),
  account_type: z.string().min(1, 'Account type is required'),
  contact_person: z.string().optional(),
  mobile: z.string().optional(),
  mobile_country_code: z.string().optional(),
  mobile_e164: z.string().optional(),
  office_phone: z.string().optional(),
  office_phone_country_code: z.string().optional(),
  office_phone_e164: z.string().optional(),
  email: z.string().email('Invalid email').optional().or(z.literal('')),
  website: z.string().optional(),
  gstin: z.string().optional(),
  gst_registration_type: z.string().optional(),
  pan: z.string().optional(),
  tan: z.string().optional(),
  state: z.string().min(1, 'State is required'),
  state_code: z.string().min(1, 'State code is required'),
  bank_account_type: z.string().optional(),
});

type PartyForm = z.infer<typeof partySchema>;

export default function PartiesPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const [gstinValid, setGstinValid] = useState(false);

  const { data: parties = [], isLoading } = useQuery({
    queryKey: ['parties'],
    queryFn: () => partiesApi.getAll()
  });

  const { register, handleSubmit, watch, setValue, control, formState: { errors }, reset } = useForm<PartyForm>({
    resolver: zodResolver(partySchema),
    defaultValues: {
      party_type: 'BUSINESS',
      account_type: 'CUSTOMER',
      gst_registration_type: 'UNREGISTERED',
      state: 'Karnataka',
      state_code: '29',
      mobile_country_code: '+91',
      office_phone_country_code: '+91',
    }
  });

  const createMutation = useMutation({
    mutationFn: partiesApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['parties'] });
      setIsModalOpen(false);
      reset();
      setGstinValid(false);
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create party');
    }
  });

  const onSubmit = (data: PartyForm) => {
    setApiError(null);
    createMutation.mutate(data);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Customers & Suppliers</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage your sundry debtors and creditors.</p>
        </div>
        <Button onClick={() => { setIsModalOpen(true); reset(); setGstinValid(false); }}>Add New Party</Button>
      </div>

      {isLoading ? (
        <div>Loading parties...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Party Name</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">GSTIN / Status</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Contact</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">State</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {parties.map((party) => (
                <tr key={party.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-foreground">{party.legal_name}</div>
                    {party.trade_name && <div className="text-xs text-muted-foreground">{party.trade_name}</div>}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${party.account_type === 'CUSTOMER' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'}`}>
                      {party.account_type}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-foreground">{party.gstin || 'No GSTIN'}</div>
                    <div className="text-xs text-muted-foreground">{party.gst_registration_type}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    <div>{party.contact_person || '-'}</div>
                    <div>{party.mobile || '-'}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {party.state} ({party.state_code})
                  </td>
                </tr>
              ))}
              {parties.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-muted-foreground">
                    No parties found. Click "Add New Party" to create one.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setIsModalOpen(false)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4 border-b pb-2">Add New Party</h3>
              
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Basic Details */}
                  <div className="md:col-span-2 grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Account Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('account_type')}>
                        <option value="CUSTOMER">Customer (Debtor)</option>
                        <option value="VENDOR">Vendor (Creditor)</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Party Type</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('party_type')}>
                        <option value="BUSINESS">Business (B2B)</option>
                        <option value="INDIVIDUAL">Individual (B2C)</option>
                      </select>
                    </div>
                  </div>

                  <Input label="Legal Name" {...register('legal_name')} error={errors.legal_name?.message} />
                  <Input label="Trade Name (Optional)" {...register('trade_name')} error={errors.trade_name?.message} />
                  
                  {/* Tax Details */}
                  <div className="md:col-span-2 bg-muted p-4 rounded-md border border">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Tax & Location Details</h4>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium text-muted-foreground mb-1">GST Registration</label>
                        <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('gst_registration_type')}>
                          <option value="REGISTERED">Registered Regular</option>
                          <option value="COMPOSITION">Registered Composition</option>
                          <option value="UNREGISTERED">Unregistered</option>
                          <option value="CONSUMER">Consumer</option>
                        </select>
                      </div>
                      
                      <Controller
                        name="gstin"
                        control={control}
                        render={({ field }) => (
                          <GSTINInput
                            label="GSTIN"
                            value={field.value || ''}
                            onChange={(v) => field.onChange(v)}
                            error={errors.gstin?.message}
                            onValidated={(parsed, valid) => {
                              if (valid && parsed) {
                                setValue('state_code', parsed.stateCode, { shouldValidate: true });
                                setValue('state', parsed.stateName || '', { shouldValidate: true });
                                setValue('pan', parsed.pan, { shouldValidate: true });
                                setGstinValid(true);
                              } else {
                                setGstinValid(false);
                              }
                            }}
                          />
                        )}
                      />
                      
                      <Input 
                        label="PAN" 
                        {...register('pan')} 
                        error={errors.pan?.message}
                        disabled={gstinValid}
                        className={gstinValid ? "bg-gray-100" : ""}
                      />

                      <Input label="TAN" {...register('tan')} error={errors.tan?.message} />
                      
                      <div className="grid grid-cols-2 gap-2 col-span-2 md:col-span-1">
                        <Input 
                          label="State" 
                          {...register('state')} 
                          error={errors.state?.message} 
                          placeholder="e.g. Karnataka"
                          readOnly={gstinValid}
                          className={gstinValid ? "bg-muted cursor-not-allowed" : ""}
                        />
                        <Input 
                          label="State Code" 
                          {...register('state_code')} 
                          error={errors.state_code?.message} 
                          placeholder="e.g. 29"
                          readOnly={gstinValid}
                          className={gstinValid ? "bg-muted cursor-not-allowed" : ""}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Bank Details */}
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Bank Information</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <BankAccountTypeSelect 
                        label="Bank Account Type" 
                        {...register('bank_account_type')} 
                        error={errors.bank_account_type?.message} 
                      />
                    </div>
                  </div>

                  {/* Contact Details */}
                  <div className="md:col-span-2">
                    <h4 className="text-sm font-semibold text-muted-foreground mb-3">Contact Information</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <Input label="Contact Person" {...register('contact_person')} error={errors.contact_person?.message} />
                      
                      <PhoneInput 
                        label="Mobile Number" 
                        value={watch('mobile') || ''} 
                        countryCode={watch('mobile_country_code') || '+91'} 
                        onValueChange={(phone, cc, e164, _iso) => { 
                          setValue('mobile', phone); 
                          setValue('mobile_country_code', cc); 
                          setValue('mobile_e164', e164); 
                        }} 
                        error={errors.mobile?.message}
                      />

                      <PhoneInput 
                        label="Office Contact" 
                        optional 
                        value={watch('office_phone') || ''} 
                        countryCode={watch('office_phone_country_code') || '+91'} 
                        onValueChange={(phone, cc, e164, _iso) => { 
                          setValue('office_phone', phone); 
                          setValue('office_phone_country_code', cc); 
                          setValue('office_phone_e164', e164); 
                        }} 
                        error={errors.office_phone?.message}
                      />

                      <Input label="Email Address" type="email" {...register('email')} error={errors.email?.message} />
                      
                      <Input label="Website" type="url" {...register('website')} placeholder="https://..." error={errors.website?.message} />
                    </div>
                  </div>
                </div>

                <div className="pt-4 border-t flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Party</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/master/UnitsPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { unitsApi } from '../../api/units';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const unitSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  abbreviation: z.string().min(1, 'Abbreviation is required'),
  category: z.string().min(1, 'Category is required'),
  is_base_unit: z.boolean(),
  base_unit_id: z.string().optional(),
  multiplier: z.coerce.number().optional(),
  formula: z.string().optional(),
  aliases: z.string().optional(),
});

type UnitForm = z.infer<typeof unitSchema>;

export default function UnitsPage() {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: units = [], isLoading } = useQuery({
    queryKey: ['units'],
    queryFn: unitsApi.getAll
  });

  const { register, handleSubmit, watch, formState: { errors }, reset } = useForm<any>({
    resolver: zodResolver(unitSchema),
    defaultValues: {
      is_base_unit: true,
      multiplier: 1
    }
  });

  const isBaseUnit = watch('is_base_unit');

  const createMutation = useMutation({
    mutationFn: unitsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
      setIsModalOpen(false);
      reset();
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create unit');
    }
  });

  const deleteMutation = useMutation({
    mutationFn: unitsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    }
  });

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate({
      ...(data as UnitForm),
      base_unit_id: data.base_unit_id ? parseInt(data.base_unit_id) : null,
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Units of Measurement</h2>
          <p className="mt-1 text-sm text-muted-foreground">Manage base units, derived units, and custom conversion formulas.</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)}>Add New Unit</Button>
      </div>

      {isLoading ? (
        <div>Loading units...</div>
      ) : (
        <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
          <table className="min-w-full divide-y divide-border">
            <thead className="bg-muted/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Unit</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Abbreviation</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Category</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Formula / Multiplier</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-card divide-y divide-border">
              {units.map((unit) => (
                <tr key={unit.id}>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-foreground">{unit.name}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{unit.abbreviation}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{unit.category}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {unit.is_base_unit ? (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Base</span>
                    ) : (
                      <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">Derived</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">
                    {unit.formula ? (
                      <code className="text-xs bg-muted px-1 py-0.5 rounded">{unit.formula}</code>
                    ) : unit.multiplier !== 1 ? (
                      `${unit.multiplier}x Base`
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button 
                      onClick={() => {
                        if (confirm('Are you sure you want to delete this unit?')) {
                          deleteMutation.mutate(unit.id);
                        }
                      }}
                      className="text-red-600 hover:text-red-900"
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {isModalOpen && (
        <div className="fixed inset-0 z-10 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity bg-black/60" onClick={() => setIsModalOpen(false)}></div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
            <div className="inline-block px-4 pt-5 pb-4 overflow-hidden text-left align-bottom transition-all transform bg-card rounded-xl shadow-xl sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6">
              <h3 className="text-lg font-medium leading-6 text-foreground mb-4">Add New Unit</h3>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {apiError && (
                  <div className="bg-red-50 text-red-600 p-3 rounded-md text-sm border border-red-100">
                    {apiError}
                  </div>
                )}
                
                <div className="grid grid-cols-2 gap-4">
                  <Input label="Name (e.g. Kilogram)" {...register('name')} error={errors.name?.message} />
                  <Input label="Abbreviation (e.g. KG)" {...register('abbreviation')} error={errors.abbreviation?.message} />
                </div>
                
                <Input label="Category (e.g. Weight)" {...register('category')} error={errors.category?.message} />
                
                <div className="flex items-center h-10 mt-2">
                  <input type="checkbox" id="is_base_unit" className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-input rounded" {...register('is_base_unit')} />
                  <label htmlFor="is_base_unit" className="ml-2 block text-sm text-foreground font-medium">This is a Base Unit</label>
                </div>

                {!isBaseUnit && (
                  <div className="space-y-4 p-4 bg-muted rounded-md border border">
                    <div>
                      <label className="block text-sm font-medium text-muted-foreground mb-1">Base Unit Reference</label>
                      <select className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('base_unit_id')}>
                        <option value="">Select a base unit...</option>
                        {units.filter(u => u.is_base_unit).map(u => (
                          <option key={u.id} value={u.id}>{u.name} ({u.abbreviation})</option>
                        ))}
                      </select>
                    </div>
                    <Input label="Simple Multiplier (e.g. 1000)" type="number" step="any" {...register('multiplier')} error={errors.multiplier?.message} />
                    <Input label="Or Custom Formula (e.g. PCS * 1.5)" {...register('formula')} error={errors.formula?.message} />
                  </div>
                )}

                <Input label="Aliases (comma separated)" placeholder="kg, kgs, kilo" {...register('aliases')} error={errors.aliases?.message} />

                <div className="mt-5 sm:mt-6 flex justify-end space-x-3">
                  <Button type="button" variant="secondary" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                  <Button type="submit" isLoading={createMutation.isPending}>Save Unit</Button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/orders/OrderBuilderPage.tsx
import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useNavigate, useLocation } from 'react-router-dom';
import { ordersApi, type SupplyOrderCalculateRequest, type SupplyOrderCreateRequest } from '../../api/orders';
import { itemsApi } from '../../api/items';
import { unitsApi } from '../../api/units';
import { partiesApi } from '../../api/parties';
import { quotationsApi } from '../../api/quotations';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const orderLineSchema = z.object({
  item_id: z.string().optional(),
  item_name: z.string().min(1, 'Item name is required'),
  description: z.string().optional(),
  sku: z.string().optional(),
  hsn_sac: z.string().optional(),
  quantity: z.coerce.number().min(0.001, 'Quantity must be > 0'),
  unit_id: z.string().min(1, 'Unit is required'),
  unit_name: z.string(),
  unit_symbol: z.string(),
  rate: z.coerce.number().min(0),
  discount_type: z.string().default('NONE'),
  discount_value: z.coerce.number().default(0),
  gst_rate: z.coerce.number().default(0),
});

const orderSchema = z.object({
  order_type: z.enum(['PURCHASE', 'SALES']),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  order_date: z.string().min(1, 'Date is required'),
  expected_date: z.string().optional(),
  party_id: z.string().min(1, 'Party is required'),
  place_of_supply: z.string().min(1, 'Place of supply is required'),
  lines: z.array(orderLineSchema).min(1, 'At least one line is required'),
  notes: z.string().optional(),
  terms: z.string().optional(),
});



export default function OrderBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const queryClient = useQueryClient();
  const [apiError, setApiError] = useState<string | null>(null);

  // Determine order type from URL (e.g. /supply-in/new -> PURCHASE)
  const isPurchase = location.pathname.includes('supply-in');
  const defaultOrderType = isPurchase ? 'PURCHASE' : 'SALES';

  const { data: items = [] } = useQuery({ queryKey: ['items'], queryFn: itemsApi.getAll });
  const { data: units = [] } = useQuery({ queryKey: ['units'], queryFn: unitsApi.getAll });
  const { data: parties = [] } = useQuery({ 
    queryKey: ['parties', isPurchase ? 'VENDOR' : 'CUSTOMER'], 
    queryFn: () => partiesApi.getAll(isPurchase ? 'VENDOR' : 'CUSTOMER') 
  });

  const searchParams = new URLSearchParams(location.search);
  const quotationId = searchParams.get('quotation_id');

  const { data: quotation } = useQuery({
    queryKey: ['quotations', quotationId],
    queryFn: () => quotationsApi.getById(quotationId!),
    enabled: !!quotationId
  });

  const { register, control, handleSubmit, watch, setValue, reset, formState: { errors } } = useForm<any>({
    resolver: zodResolver(orderSchema),
    defaultValues: {
      order_type: defaultOrderType,
      tax_treatment: 'GST',
      order_date: new Date().toISOString().split('T')[0],
      expected_date: '',
      place_of_supply: '',
      lines: [{ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0, unit_name: '', unit_symbol: '', unit_id: '' }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const watchAll = watch();
  const taxTreatment = watchAll.tax_treatment;

  // Pre-fill form if quotation is loaded
  useEffect(() => {
    if (quotation && units.length > 0) {
      reset({
        quotation_id: quotation.id,
        order_type: quotation.quotation_type,
        tax_treatment: quotation.tax_treatment,
        order_date: new Date().toISOString().split('T')[0],
        expected_date: '',
        party_id: quotation.party_id,
        place_of_supply: quotation.place_of_supply,
        notes: quotation.notes || '',
        terms: quotation.terms || '',
        lines: quotation.lines.map((l: any) => {
          const unit = units.find((u: any) => String(u.id) === String(l.unit_id));
          return {
            item_id: l.item_id || '',
            item_name: l.item_name_snapshot,
            sku: l.sku_snapshot || '',
            hsn_sac: l.hsn_sac_snapshot || '',
            description: l.description || '',
            quantity: l.quantity,
            unit_id: l.unit_id || '',
            unit_name: unit?.name || l.unit_snapshot || '',
            unit_symbol: unit?.abbreviation || l.unit_snapshot || '',
            rate: l.rate,
            discount_type: l.discount_type || 'NONE',
            discount_value: l.discount_value || 0,
            gst_rate: l.gst_rate || 0
          };
        })
      });
    }
  }, [quotation, units, reset]);

  const calculateMutation = useMutation({
    mutationFn: ordersApi.calculate,
  });

  const createMutation = useMutation({
    mutationFn: ordersApi.create,
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      alert(`Order Draft Created! ID: ${data.id}`);
      navigate(isPurchase ? '/supply-in' : '/supply-out');
    },
    onError: (error: any) => {
      setApiError(error.message || 'Failed to create order');
    }
  });

  // Debounced calculate
  useEffect(() => {
    if (!watchAll.lines || watchAll.lines.length === 0) return;
    
    // Quick validation before hitting backend
    const isValidForCalc = watchAll.lines.every((l: any) => l.item_name && l.quantity > 0 && l.unit_id);
    if (!isValidForCalc) return;

    const timeoutId = setTimeout(() => {
      const calcData: SupplyOrderCalculateRequest = {
        tax_treatment: watchAll.tax_treatment as 'GST' | 'WITHOUT_GST',
        party_id: watchAll.party_id || null,
        place_of_supply: watchAll.place_of_supply || '29', // Default state code fallback
        lines: watchAll.lines.map((l: any) => ({
          item_id: l.item_id,
          item_name: l.item_name,
          sku: l.sku,
          description: l.description,
          hsn_sac: l.hsn_sac,
          quantity: Number(l.quantity) || 0,
          unit_id: l.unit_id,
          unit_name: l.unit_name || 'Unit',
          unit_symbol: l.unit_symbol || 'U',
          rate: Number(l.rate) || 0,
          discount_type: l.discount_type,
          discount_value: Number(l.discount_value) || 0,
          gst_rate: Number(l.gst_rate) || 0,
        }))
      };
      
      calculateMutation.mutate(calcData);
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [JSON.stringify(watchAll.lines), watchAll.party_id, watchAll.place_of_supply, watchAll.tax_treatment]);

  const handleItemSelect = (index: number, itemId: string) => {
    const item = items.find((i: any) => i.id.toString() === itemId);
    if (item) {
      setValue(`lines.${index}.item_id`, item.id.toString());
      setValue(`lines.${index}.item_name`, item.name);
      setValue(`lines.${index}.sku`, item.sku || '');
      setValue(`lines.${index}.description`, item.description || '');
      setValue(`lines.${index}.hsn_sac`, item.hsn_sac || '');
      setValue(`lines.${index}.rate`, isPurchase ? (item.purchase_price || 0) : item.sale_price);
      setValue(`lines.${index}.gst_rate`, item.gst_rate);
      
      const unit = units.find((u: any) => u.id === item.unit_id);
      if (unit) {
        setValue(`lines.${index}.unit_id`, unit.id.toString());
        setValue(`lines.${index}.unit_name`, unit.name);
        setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
      }
    }
  };

  const handlePartySelect = (partyId: string) => {
    const party = parties.find((p: any) => p.id === partyId);
    if (party) {
      setValue('place_of_supply', party.state_code);
    }
  };

  const handleUnitSelect = (index: number, unitId: string) => {
    const unit = units.find((u: any) => u.id.toString() === unitId);
    if (unit) {
      setValue(`lines.${index}.unit_id`, unit.id.toString());
      setValue(`lines.${index}.unit_name`, unit.name);
      setValue(`lines.${index}.unit_symbol`, unit.abbreviation);
    }
  };

  const onSubmit = (data: any) => {
    setApiError(null);
    createMutation.mutate(data as SupplyOrderCreateRequest);
  };

  const calcData = calculateMutation.data;
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  return (
    <div className="max-w-6xl mx-auto space-y-6 pb-20">
      <div className="flex justify-between items-center border-b pb-4">
        <div>
          <h2 className="text-2xl font-bold text-foreground">
            {isPurchase ? 'Create Supply In (Purchase Order)' : 'Create Supply Out (Sales Order)'}
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {quotationId ? 'Draft a new order from accepted quotation.' : `Draft a new ${isPurchase ? 'purchase' : 'sales'} order.`}
          </p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
        {apiError && (
          <div className="bg-red-50 text-red-600 p-4 rounded-md text-sm border border-red-100 font-medium">
            Error: {apiError}
          </div>
        )}

        {/* Header Information */}
        <div className="bg-card p-6 rounded-lg shadow-sm border grid grid-cols-1 md:grid-cols-4 gap-6">
          
          <div className="md:col-span-4 border-b pb-4 mb-2 flex space-x-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Order Type</label>
              <div className="flex items-center space-x-2 mt-2">
                <input type="radio" value="PURCHASE" disabled {...register('order_type')} /> <span className="text-sm">Purchase Order</span>
                <input type="radio" value="SALES" disabled {...register('order_type')} className="ml-4" /> <span className="text-sm">Sales Order</span>
              </div>
            </div>
            
            <div className="pl-6 border-l">
              <label className="block text-sm font-medium text-muted-foreground mb-1">Tax Treatment</label>
              <div className="flex items-center space-x-2 mt-2">
                <input type="radio" value="GST" {...register('tax_treatment')} /> <span className="text-sm">GST</span>
                <input type="radio" value="WITHOUT_GST" {...register('tax_treatment')} className="ml-4" /> <span className="text-sm">Without GST</span>
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-muted-foreground mb-1">{partyLabel}</label>
            <select 
              className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500"
              {...register('party_id')}
              onChange={(e) => {
                register('party_id').onChange(e);
                handlePartySelect(e.target.value);
              }}
            >
              <option value="">Select {partyLabel}...</option>
              {parties.map((p: any) => (
                <option key={p.id} value={p.id}>{p.legal_name} {p.gstin ? `(${p.gstin})` : ''}</option>
              ))}
            </select>
            {errors.party_id?.message && <p className="mt-1 text-sm text-red-600">{errors.party_id.message as string}</p>}
          </div>

          <Input label="Order Date" type="date" {...register('order_date')} error={errors.order_date?.message} />
          <Input label="Expected Date" type="date" {...register('expected_date')} error={errors.expected_date?.message} />
          
          <div className="md:col-span-2">
            <Input label="Place of Supply (State Code)" {...register('place_of_supply')} error={errors.place_of_supply?.message} placeholder="e.g. 29" />
          </div>
        </div>

        {/* Invoice Lines */}
        <div className="bg-card p-6 rounded-lg shadow-sm border space-y-4">
          <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Items & Services</h3>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-border text-sm">
              <thead className="bg-muted/50">
                <tr>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-1/4">Item / Product</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-24">HSN/SKU</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Qty</th>
                  <th className="px-3 py-2 text-left font-medium text-muted-foreground w-28">Unit</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-28">Rate (₹)</th>
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-24">Discount</th>
                  {taxTreatment === 'GST' && <th className="px-3 py-2 text-right font-medium text-muted-foreground w-20">GST %</th>}
                  <th className="px-3 py-2 text-right font-medium text-muted-foreground w-32">Amount</th>
                  <th className="px-3 py-2 w-10"></th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {fields.map((field, index) => {
                  const calculatedLine = calcData?.lines?.[index];
                  return (
                    <tr key={field.id} className="hover:bg-muted/50">
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1 mb-1"
                          onChange={(e) => handleItemSelect(index, e.target.value)}
                        >
                          <option value="">Select Item...</option>
                          {items.map((i: any) => (
                            <option key={i.id} value={i.id}>{i.name}</option>
                          ))}
                        </select>
                        <input type="text" placeholder="Item Name" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.item_name`)} />
                      </td>
                      <td className="px-3 py-2 space-y-1">
                        <input type="text" placeholder="HSN" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.hsn_sac`)} />
                        <input type="text" placeholder="SKU" className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.sku`)} />
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.quantity`)} />
                      </td>
                      <td className="px-3 py-2">
                        <select 
                          className="block w-full rounded border-input shadow-sm text-sm border px-2 py-1"
                          {...register(`lines.${index}.unit_id`)}
                          onChange={(e) => {
                            register(`lines.${index}.unit_id`).onChange(e);
                            handleUnitSelect(index, e.target.value);
                          }}
                        >
                          <option value="">Unit...</option>
                          {units.map((u: any) => (
                            <option key={u.id} value={u.id}>{u.abbreviation}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-3 py-2">
                        <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.rate`)} />
                      </td>
                      <td className="px-3 py-2">
                        <div className="flex space-x-1">
                          <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.discount_value`)} />
                          <select className="block rounded border-input shadow-sm text-xs border px-1 py-1 bg-muted/50" {...register(`lines.${index}.discount_type`)}>
                            <option value="NONE">None</option>
                            <option value="PERCENT">%</option>
                            <option value="FIXED">₹</option>
                          </select>
                        </div>
                      </td>
                      {taxTreatment === 'GST' && (
                        <td className="px-3 py-2">
                          <input type="number" step="any" className="block w-full text-right rounded border-input shadow-sm text-sm border px-2 py-1" {...register(`lines.${index}.gst_rate`)} />
                        </td>
                      )}
                      <td className="px-3 py-2 text-right font-medium text-foreground bg-muted/50">
                        {calculateMutation.isPending ? '...' : (calculatedLine?.line_total ? `₹${calculatedLine.line_total.toFixed(2)}` : '₹0.00')}
                      </td>
                      <td className="px-3 py-2 text-center">
                        <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 font-bold p-1">×</button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          
          <Button 
            type="button" 
            variant="secondary" 
            onClick={() => append({ item_name: '', quantity: 1, rate: 0, discount_type: 'NONE', discount_value: 0, gst_rate: 0, unit_name: '', unit_symbol: '', unit_id: '' })}
          >
            + Add Line
          </Button>
        </div>

        {/* Totals & Notes */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Order Notes</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('notes')} />
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Terms & Conditions</label>
              <textarea rows={3} className="block w-full rounded-lg border text-sm px-3 py-2 outline-none transition-colors bg-background border-input focus:border-slate-500" {...register('terms')} />
            </div>
          </div>

          <div className="bg-card p-6 rounded-lg shadow-sm border">
            <h3 className="text-lg font-medium text-foreground border-b pb-2 mb-4">Order Summary</h3>
            
            <div className="space-y-3 text-sm">
              <div className="flex justify-between text-muted-foreground">
                <span>Gross Amount</span>
                <span>₹{(calcData?.subtotal || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-red-600">
                <span>Discount</span>
                <span>- ₹{(calcData?.discount_total || 0).toFixed(2)}</span>
              </div>
              <div className="flex justify-between text-foreground font-medium pt-2 border-t">
                <span>{taxTreatment === 'GST' ? 'Taxable Value' : 'Net Amount'}</span>
                <span>₹{(calcData?.taxable_total || 0).toFixed(2)}</span>
              </div>
              
              {taxTreatment === 'GST' && (
                <>
                  {(calcData?.igst_total || 0) > 0 ? (
                    <div className="flex justify-between text-muted-foreground">
                      <span>IGST</span>
                      <span>₹{(calcData?.igst_total || 0).toFixed(2)}</span>
                    </div>
                  ) : (
                    <>
                      <div className="flex justify-between text-muted-foreground">
                        <span>CGST</span>
                        <span>₹{(calcData?.cgst_total || 0).toFixed(2)}</span>
                      </div>
                      <div className="flex justify-between text-muted-foreground">
                        <span>SGST / UTGST</span>
                        <span>₹{(calcData?.sgst_total || 0).toFixed(2)}</span>
                      </div>
                    </>
                  )}
                </>
              )}

              <div className="flex justify-between text-xl font-bold text-foreground pt-4 border-t mt-4">
                <span>Grand Total</span>
                <span>₹{(calcData?.grand_total || 0).toFixed(2)}</span>
              </div>

              {calcData?.amount_in_words && (
                <div className="text-xs text-muted-foreground text-right italic mt-1">
                  Rupees {calcData.amount_in_words}
                </div>
              )}
            </div>
          </div>
        </div>

        <div className="fixed bottom-0 left-0 right-0 bg-card border-t p-4 shadow-lg flex justify-end space-x-4 z-10 md:ml-64">
          <Button type="button" variant="secondary" onClick={() => navigate(isPurchase ? '/supply-in' : '/supply-out')}>Cancel</Button>
          <Button type="submit" isLoading={createMutation.isPending} disabled={calculateMutation.isPending || !calcData?.grand_total}>
            Save Draft Order
          </Button>
        </div>
      </form>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/orders/OrderListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Link, useLocation } from 'react-router-dom';
import { ordersApi, type SupplyOrderResponse } from '../../api/orders';
import { Button } from '../../components/common/Button';

export default function OrderListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedOrder, setSelectedOrder] = useState<SupplyOrderResponse | null>(null);

  const isPurchase = location.pathname.includes('supply-in');
  const orderType = isPurchase ? 'PURCHASE' : 'SALES';
  const pageTitle = isPurchase ? 'Supply In (Purchase Orders)' : 'Supply Out (Sales Orders)';
  const newLink = isPurchase ? '/supply-in/new' : '/supply-out/new';
  const partyLabel = isPurchase ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['orders', orderType],
    queryFn: () => ordersApi.getAll(orderType)
  });

  const confirmMutation = useMutation({
    mutationFn: ordersApi.confirm,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      setSelectedOrder(null);
    }
  });

  const convertMutation = useMutation({
    mutationFn: ordersApi.convert,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['orders'] });
      queryClient.invalidateQueries({ queryKey: ['invoices'] });
      alert('Order successfully converted to ' + (isPurchase ? 'Purchase Bill' : 'Sales Invoice') + '!');
      setSelectedOrder(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {orderType.toLowerCase()} orders.
          </p>
        </div>
        <Link to={newLink}>
          <Button>Create {isPurchase ? 'Purchase' : 'Sales'} Order</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Order No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Tax Type</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading orders...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No {orderType.toLowerCase()} orders found.</td></tr>
            ) : (
              data?.items.map((order) => (
                <tr key={order.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{order.order_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{order.order_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{order.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${order.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        order.status === 'CONFIRMED' ? 'bg-blue-100 text-blue-800' : 
                        order.status === 'CANCELLED' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'}`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{order.tax_treatment.replace('_', ' ')}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{order.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedOrder(order)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedOrder && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedOrder.order_number || 'Draft Order'}
                </h3>
                <p className="text-sm text-muted-foreground">Date: {selectedOrder.order_date} | Type: {selectedOrder.order_type} | Tax: {selectedOrder.tax_treatment.replace('_', ' ')}</p>
              </div>
              <button onClick={() => setSelectedOrder(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    {selectedOrder.tax_treatment === 'GST' && (
                      <>
                        <th className="px-4 py-2 text-right text-muted-foreground font-medium">Taxable</th>
                        <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                      </>
                    )}
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedOrder.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">{line.item_name_snapshot}</td>
                      <td className="px-4 py-2 text-right">{line.quantity} {line.unit_symbol_snapshot}</td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      {selectedOrder.tax_treatment === 'GST' && (
                        <>
                          <td className="px-4 py-2 text-right">₹{line.taxable_value.toFixed(2)}</td>
                          <td className="px-4 py-2 text-right">{line.gst_rate}% (₹{(line.cgst_amount+line.sgst_amount+line.igst_amount).toFixed(2)})</td>
                        </>
                      )}
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex justify-end">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedOrder.subtotal.toFixed(2)}</span>
                  </div>
                  {selectedOrder.tax_treatment === 'GST' && (
                    <>
                      {selectedOrder.igst_total > 0 ? (
                        <div className="flex justify-between">
                          <span className="text-muted-foreground">IGST</span>
                          <span>₹{selectedOrder.igst_total.toFixed(2)}</span>
                        </div>
                      ) : (
                        <>
                          <div className="flex justify-between">
                            <span className="text-muted-foreground">CGST</span>
                            <span>₹{selectedOrder.cgst_total.toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-muted-foreground">SGST</span>
                            <span>₹{selectedOrder.sgst_total.toFixed(2)}</span>
                          </div>
                        </>
                      )}
                    </>
                  )}
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedOrder.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedOrder(null)}>Close</Button>
              {selectedOrder.status === 'DRAFT' && (
                <Button 
                  onClick={() => confirmMutation.mutate(selectedOrder.id)}
                  isLoading={confirmMutation.isPending}
                >
                  Confirm Order
                </Button>
              )}
              {selectedOrder.status === 'CONFIRMED' && (
                <Button 
                  onClick={() => convertMutation.mutate(selectedOrder.id)}
                  isLoading={convertMutation.isPending}
                >
                  Convert to {isPurchase ? 'Purchase Bill' : 'Sales Invoice'}
                </Button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/quotations/QuotationBuilderPage.tsx
import { useNavigate, useLocation } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { quotationsApi, type QuotationCreateRequest } from '../../api/quotations';
import { partiesApi } from '../../api/parties';
import { itemsApi } from '../../api/items';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const quotationLineSchema = z.object({
  item_id: z.string().optional(),
  item_name_snapshot: z.string().min(1, 'Item name is required'),
  description: z.string().optional(),
  quantity: z.number().min(0.001, 'Quantity must be greater than 0'),
  rate: z.number().min(0, 'Rate must be >= 0'),
  discount_type: z.string().optional(),
  discount_value: z.number().optional().default(0),
  gst_rate: z.number().optional().default(0),
});

const quotationSchema = z.object({
  party_id: z.string().min(1, 'Party is required'),
  tax_treatment: z.enum(['GST', 'WITHOUT_GST']),
  valid_until: z.string().min(1, 'Valid until date is required'),
  place_of_supply: z.string().min(1, 'Place of supply is required'),
  notes: z.string().optional(),
  terms: z.string().optional(),
  lines: z.array(quotationLineSchema).min(1, 'At least one item is required'),
});

export default function QuotationBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const isSupplyIn = location.pathname.includes('supply-in');
  const quotationType = isSupplyIn ? 'PURCHASE' : 'SALES';
  
  const { data: parties } = useQuery({
    queryKey: ['parties'],
    queryFn: () => partiesApi.getAll()
  });

  const { data: items } = useQuery({
    queryKey: ['items'],
    queryFn: () => itemsApi.getAll()
  });

  const { register, control, handleSubmit, watch, setValue, formState: { errors } } = useForm<any>({
    resolver: zodResolver(quotationSchema),
    defaultValues: {
      tax_treatment: 'GST',
      valid_until: new Date(Date.now() + 30*24*60*60*1000).toISOString().split('T')[0],
      place_of_supply: 'State',
      lines: [{ item_name_snapshot: '', quantity: 1, rate: 0, discount_value: 0, gst_rate: 18 }]
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const watchTaxTreatment = watch('tax_treatment');

  const createMutation = useMutation({
    mutationFn: quotationsApi.create,
    onSuccess: () => {
      navigate(`${isSupplyIn ? '/supply-in' : '/supply-out'}/quotations`);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to create quotation");
    }
  });

  const handleItemSelect = (index: number, itemId: string) => {
    const item = items?.find((i: any) => i.id === itemId || String(i.id) === itemId);
    if (item) {
      setValue(`lines.${index}.item_id`, String(item.id));
      setValue(`lines.${index}.item_name_snapshot`, item.name);
      setValue(`lines.${index}.rate`, isSupplyIn ? (item.purchase_price || 0) : (item.sale_price || 0));
      if (watchTaxTreatment === 'GST') {
        setValue(`lines.${index}.gst_rate`, item.gst_rate || 18);
      }
    }
  };

  const onSubmit = (data: any) => {
    const request: QuotationCreateRequest = {
      ...data,
      quotation_type: quotationType,
      lines: data.lines.map((l: any) => ({
        ...l,
        discount_type: l.discount_value > 0 ? 'FIXED' : null
      }))
    };
    createMutation.mutate(request);
  };

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">
          Create {isSupplyIn ? 'Purchase Quotation' : 'Sales Quotation'}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Create a non-binding quotation for your {isSupplyIn ? 'supplier' : 'customer'}.
        </p>
      </div>

      <div className="bg-card rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="col-span-2">
              <label className="block text-sm font-medium text-muted-foreground mb-1">
                {isSupplyIn ? 'Supplier' : 'Customer'} *
              </label>
              <select
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                {...register('party_id')}
              >
                <option value="">-- Select Party --</option>
                {parties?.map((p: any) => (
                  <option key={p.id} value={p.id}>{p.legal_name || p.name}</option>
                ))}
              </select>
              {errors.party_id && <p className="text-red-500 text-xs mt-1">{errors.party_id.message as string}</p>}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Tax Treatment</label>
              <select
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                {...register('tax_treatment')}
              >
                <option value="GST">GST</option>
                <option value="WITHOUT_GST">Without GST</option>
              </select>
            </div>

            <Input
              label="Valid Until *"
              type="date"
              {...register('valid_until')}
              error={errors.valid_until?.message as string}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input
              label="Place of Supply *"
              {...register('place_of_supply')}
              error={errors.place_of_supply?.message as string}
            />
          </div>

          <div className="mt-8 border-t pt-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-foreground">Quotation Items</h3>
              <Button type="button" variant="secondary" onClick={() => append({ item_name_snapshot: '', quantity: 1, rate: 0, discount_value: 0, gst_rate: 18 })}>
                + Add Row
              </Button>
            </div>
            
            <div className="overflow-x-auto border rounded-lg">
              <table className="min-w-full divide-y divide-border">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase">Item Selection</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase w-48">Item Name *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase w-24">Qty *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase w-32">Rate *</th>
                    <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase w-32">Disc (₹)</th>
                    {watchTaxTreatment === 'GST' && (
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase w-24">GST %</th>
                    )}
                    <th className="px-4 py-3"></th>
                  </tr>
                </thead>
                <tbody className="bg-card divide-y divide-border">
                  {fields.map((field, index) => (
                    <tr key={field.id}>
                      <td className="px-4 py-2">
                        <select 
                          className="w-full text-sm rounded border-input"
                          onChange={(e) => handleItemSelect(index, e.target.value)}
                        >
                          <option value="">-- Catalog --</option>
                          {items?.map((i: any) => (
                            <option key={i.id} value={i.id}>{i.name}</option>
                          ))}
                        </select>
                      </td>
                      <td className="px-4 py-2">
                        <input
                          {...register(`lines.${index}.item_name_snapshot`)}
                          className="w-full text-sm rounded border-input"
                          placeholder="Manual name"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.quantity`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-input"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.rate`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-input"
                        />
                      </td>
                      <td className="px-4 py-2">
                        <input
                          type="number" step="any" min="0"
                          {...register(`lines.${index}.discount_value`, { valueAsNumber: true })}
                          className="w-full text-sm rounded border-input"
                        />
                      </td>
                      {watchTaxTreatment === 'GST' && (
                        <td className="px-4 py-2">
                          <input
                            type="number" step="any" min="0"
                            {...register(`lines.${index}.gst_rate`, { valueAsNumber: true })}
                            className="w-full text-sm rounded border-input"
                          />
                        </td>
                      )}
                      <td className="px-4 py-2 text-right">
                        <button type="button" onClick={() => remove(index)} className="text-red-500 hover:text-red-700 text-xl font-bold">&times;</button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {errors.lines && <p className="text-red-500 text-xs p-4">{errors.lines.message as string}</p>}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Notes / Remarks</label>
              <textarea
                {...register('notes')}
                rows={3}
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Terms & Conditions</label>
              <textarea
                {...register('terms')}
                rows={3}
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
          </div>

          <div className="flex justify-end space-x-4 pt-6 border-t">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate(-1)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={createMutation.isPending}
            >
              Create Quotation
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/quotations/QuotationListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { quotationsApi, type QuotationResponse } from '../../api/quotations';
import { Button } from '../../components/common/Button';

export default function QuotationListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedQuotation, setSelectedQuotation] = useState<QuotationResponse | null>(null);

  const isSupplyIn = location.pathname.includes('supply-in');
  const quotationType = isSupplyIn ? 'PURCHASE' : 'SALES';
  const pageTitle = isSupplyIn ? 'Purchase Quotations' : 'Sales Quotations';
  const partyLabel = isSupplyIn ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['quotations', quotationType],
    queryFn: () => quotationsApi.getAll(quotationType)
  });

  const approveMutation = useMutation({
    mutationFn: quotationsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quotations'] });
      setSelectedQuotation(null);
    }
  });

  const acceptMutation = useMutation({
    mutationFn: (id: string) => quotationsApi.accept(id, "USER_ACCEPTED"),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['quotations'] });
      setSelectedQuotation(null);
    }
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {quotationType.toLowerCase()} quotations.
          </p>
        </div>
        <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/quotations/new`}>
          <Button>+ Create Quotation</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Quotation No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Valid Until</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading quotations...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No quotations found.</td></tr>
            ) : (
              data?.items.map((q) => (
                <tr key={q.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{new Date(q.quotation_date).toLocaleDateString()}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{q.quotation_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{q.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    {new Date(q.valid_until).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${q.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        q.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                        q.status === 'ACCEPTED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {q.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{q.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedQuotation(q)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedQuotation && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedQuotation.quotation_number || 'Draft Quotation'}
                </h3>
                <p className="text-sm text-muted-foreground">Rev: {selectedQuotation.revision} | Valid Until: {new Date(selectedQuotation.valid_until).toLocaleDateString()}</p>
              </div>
              <button onClick={() => setSelectedQuotation(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Discount</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedQuotation.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        {line.description && <div className="text-xs text-muted-foreground">{line.description}</div>}
                      </td>
                      <td className="px-4 py-2 text-right">
                        {line.quantity} {line.unit_snapshot}
                      </td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right text-red-500">
                        {line.discount_amount > 0 ? `-₹${line.discount_amount.toFixed(2)}` : '-'}
                      </td>
                      <td className="px-4 py-2 text-right">{line.gst_rate}%</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex justify-end">
                <div className="w-64 space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedQuotation.subtotal.toFixed(2)}</span>
                  </div>
                  {selectedQuotation.discount_total > 0 && (
                    <div className="flex justify-between text-red-600">
                      <span>Total Discount</span>
                      <span>-₹{selectedQuotation.discount_total.toFixed(2)}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Taxable Value</span>
                    <span>₹{selectedQuotation.taxable_total.toFixed(2)}</span>
                  </div>
                  {selectedQuotation.tax_treatment === 'GST' && (
                    <>
                      {selectedQuotation.cgst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>CGST</span>
                          <span>₹{selectedQuotation.cgst_total.toFixed(2)}</span>
                        </div>
                      )}
                      {selectedQuotation.sgst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>SGST</span>
                          <span>₹{selectedQuotation.sgst_total.toFixed(2)}</span>
                        </div>
                      )}
                      {selectedQuotation.igst_total > 0 && (
                        <div className="flex justify-between text-muted-foreground text-xs">
                          <span>IGST</span>
                          <span>₹{selectedQuotation.igst_total.toFixed(2)}</span>
                        </div>
                      )}
                    </>
                  )}
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedQuotation.grand_total.toFixed(2)}</span>
                  </div>
                </div>
              </div>

              {selectedQuotation.notes && (
                <div className="mt-6 p-4 bg-yellow-50 text-yellow-800 text-sm rounded">
                  <strong>Notes:</strong> {selectedQuotation.notes}
                </div>
              )}
              {selectedQuotation.terms && (
                <div className="mt-4 p-4 bg-muted text-foreground text-sm rounded">
                  <strong>Terms & Conditions:</strong>
                  <pre className="whitespace-pre-wrap font-sans mt-2">{selectedQuotation.terms}</pre>
                </div>
              )}
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedQuotation(null)}>Close</Button>
              {selectedQuotation.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedQuotation.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Quotation
                </Button>
              )}
              {selectedQuotation.status === 'APPROVED' && (
                <Button 
                  onClick={() => acceptMutation.mutate(selectedQuotation.id)}
                  isLoading={acceptMutation.isPending}
                >
                  Accept Quotation
                </Button>
              )}
              {selectedQuotation.status === 'ACCEPTED' && !selectedQuotation.fully_converted && (
                <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/new?quotation_id=${selectedQuotation.id}`}>
                  <Button variant="default">Convert to Order</Button>
                </Link>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
```

```tsx
// File: frontend/src/features/returns/ReturnBuilderPage.tsx
import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useForm, useFieldArray } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';
import { returnsApi, type ReturnOrderCreateRequest, type ReturnableLinesResponse } from '../../api/returns';
import { ordersApi } from '../../api/orders';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';

const returnLineSchema = z.object({
  original_order_line_id: z.string().min(1),
  item_name_snapshot: z.string(),
  unit_snapshot: z.string().optional(),
  returnable_quantity: z.number(),
  rate: z.number(),
  return_quantity: z.number().min(0),
  condition: z.string().optional(),
  warehouse_action: z.string().optional(),
});

const returnSchema = z.object({
  original_order_id: z.string().min(1, 'Order ID is required'),
  reason: z.string().optional(),
  lines: z.array(returnLineSchema),
});

export default function ReturnBuilderPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const isSupplyIn = location.pathname.includes('supply-in');
  const returnType = isSupplyIn ? 'SUPPLY_IN_RETURN' : 'SUPPLY_OUT_RETURN';
  const orderType = isSupplyIn ? 'PURCHASE' : 'SALES';
  
  const [orderId, setOrderId] = useState<string>('');
  const [returnableData, setReturnableData] = useState<ReturnableLinesResponse | null>(null);

  const { data: orders } = useQuery({
    queryKey: ['orders', orderType],
    queryFn: () => ordersApi.getAll(orderType)
  });

  const { register, control, handleSubmit, setValue, watch } = useForm<any>({
    resolver: zodResolver(returnSchema),
    defaultValues: {
      original_order_id: '',
      reason: '',
      lines: []
    }
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'lines'
  });

  const fetchLinesMutation = useMutation({
    mutationFn: returnsApi.getReturnableLines,
    onSuccess: (data) => {
      setReturnableData(data);
      // Populate fields automatically
      remove();
      data.lines.forEach(line => {
        append({
          original_order_line_id: line.original_order_line_id,
          item_name_snapshot: line.item_name_snapshot,
          unit_snapshot: line.unit_symbol_snapshot || '',
          returnable_quantity: line.returnable_quantity,
          rate: line.rate,
          return_quantity: 0,
          condition: 'GOOD',
          warehouse_action: 'RETURN_TO_STOCK'
        });
      });
    },
    onError: () => {
      alert("Failed to fetch returnable lines or order not found.");
      setReturnableData(null);
    }
  });

  const handleOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setOrderId(val);
    setValue('original_order_id', val);
    if (val) {
      fetchLinesMutation.mutate(val);
    } else {
      setReturnableData(null);
      remove();
    }
  };

  const createMutation = useMutation({
    mutationFn: returnsApi.create,
    onSuccess: () => {
      navigate(`${isSupplyIn ? '/supply-in' : '/supply-out'}/returns`);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to create return");
    }
  });

  const onSubmit = (data: any) => {
    // filter out lines with 0 return qty
    const filteredLines = data.lines.filter((l: any) => l.return_quantity > 0);
    if (filteredLines.length === 0) {
      alert("Please enter a return quantity for at least one item.");
      return;
    }
    
    // validate max qty
    const invalid = filteredLines.find((l: any) => l.return_quantity > l.returnable_quantity);
    if (invalid) {
      alert(`Cannot return more than ${invalid.returnable_quantity} for ${invalid.item_name_snapshot}`);
      return;
    }
    
    const request: ReturnOrderCreateRequest = {
      original_order_id: data.original_order_id,
      return_type: returnType,
      reason: data.reason,
      lines: filteredLines.map((l: any) => ({
        original_order_line_id: l.original_order_line_id,
        return_quantity: l.return_quantity,
        condition: l.condition,
        warehouse_action: l.warehouse_action
      }))
    };
    
    createMutation.mutate(request);
  };

  const formLines = watch('lines');
  
  const estimatedTotal = formLines?.reduce((sum: number, line: any) => {
    return sum + (Number(line.return_quantity || 0) * Number(line.rate || 0));
  }, 0) || 0;

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-foreground">
          Create {isSupplyIn ? 'Purchase Return' : 'Sales Return'}
        </h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Initiate a return against a confirmed {orderType.toLowerCase()} order.
        </p>
      </div>

      <div className="bg-card rounded-lg shadow-sm border p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-muted-foreground mb-1">Select Original Order *</label>
              <select
                className="w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                value={orderId}
                onChange={handleOrderChange}
                required
              >
                <option value="">-- Select Order --</option>
                {orders?.items.filter(o => o.status === 'CONFIRMED').map(o => (
                  <option key={o.id} value={o.id}>
                    {o.order_number || 'DRAFT'} - {o.party_id.substring(0,8)} (₹{o.grand_total.toFixed(2)})
                  </option>
                ))}
              </select>
            </div>
            
            <Input
              label="Reason for Return"
              {...register('reason')}
              placeholder="e.g. Damaged goods, wrong item..."
            />
          </div>
          
          {fetchLinesMutation.isPending && (
            <div className="text-sm text-muted-foreground py-4">Fetching returnable items...</div>
          )}

          {returnableData && fields.length > 0 && (
            <div className="mt-8">
              <h3 className="text-lg font-medium text-foreground mb-4">Return Items</h3>
              
              <div className="overflow-x-auto border rounded-lg">
                <table className="min-w-full divide-y divide-border">
                  <thead className="bg-muted/50">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase">Item</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase">Returnable Max</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase">Rate</th>
                      <th className="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase">Condition</th>
                      <th className="px-4 py-3 text-right text-xs font-medium text-muted-foreground uppercase w-32">Return Qty</th>
                    </tr>
                  </thead>
                  <tbody className="bg-card divide-y divide-border">
                    {fields.map((field, index) => {
                      const line = formLines[index];
                      return (
                        <tr key={field.id} className={line.return_quantity > 0 ? 'bg-red-50' : ''}>
                          <td className="px-4 py-3 text-sm font-medium text-foreground">
                            {line.item_name_snapshot}
                          </td>
                          <td className="px-4 py-3 text-sm text-muted-foreground text-right">
                            {line.returnable_quantity} {line.unit_snapshot}
                          </td>
                          <td className="px-4 py-3 text-sm text-muted-foreground text-right">
                            ₹{line.rate.toFixed(2)}
                          </td>
                          <td className="px-4 py-3">
                            <select
                              {...register(`lines.${index}.condition`)}
                              className="text-sm rounded border-input w-full"
                            >
                              <option value="GOOD">Good / Resaleable</option>
                              <option value="DAMAGED">Damaged</option>
                              <option value="DEFECTIVE">Defective</option>
                              <option value="SCRAP">Scrap</option>
                            </select>
                          </td>
                          <td className="px-4 py-3">
                            <input
                              type="number"
                              step="0.01"
                              min="0"
                              max={line.returnable_quantity}
                              {...register(`lines.${index}.return_quantity`, { valueAsNumber: true })}
                              className="w-full rounded border-input text-right text-sm font-medium text-red-600 focus:ring-red-500 focus:border-red-500"
                            />
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>

              <div className="mt-4 flex justify-between items-center text-sm">
                <div className="text-muted-foreground italic">
                  Note: The exact tax reversals will be calculated automatically by the server.
                </div>
                <div className="font-medium text-lg">
                  Estimated Base Return Value: <span className="text-red-600">₹{estimatedTotal.toFixed(2)}</span>
                </div>
              </div>
            </div>
          )}

          {returnableData && fields.length === 0 && (
            <div className="text-sm text-red-500 py-4 font-medium">
              This order has no remaining items that can be returned.
            </div>
          )}

          <div className="flex justify-end space-x-4 pt-6 border-t">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate(-1)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={createMutation.isPending}
              disabled={!returnableData || fields.length === 0}
            >
              Create Draft Return
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

```tsx
// File: frontend/src/features/returns/ReturnListPage.tsx
import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useLocation, Link } from 'react-router-dom';
import { returnsApi, type ReturnOrderResponse } from '../../api/returns';
import { Button } from '../../components/common/Button';

export default function ReturnListPage() {
  const location = useLocation();
  const queryClient = useQueryClient();
  const [selectedReturn, setSelectedReturn] = useState<ReturnOrderResponse | null>(null);
  const [showSettlementModal, setShowSettlementModal] = useState(false);
  const [settlementForm, setSettlementForm] = useState({
    settlement_type: 'ADJUST_RECEIVABLE',
    amount: 0,
    reference_number: '',
    notes: ''
  });

  const isSupplyIn = location.pathname.includes('supply-in');
  const returnType = isSupplyIn ? 'SUPPLY_IN_RETURN' : 'SUPPLY_OUT_RETURN';
  const pageTitle = isSupplyIn ? 'Purchase Returns (Supply In)' : 'Sales Returns (Supply Out)';
  const partyLabel = isSupplyIn ? 'Supplier' : 'Customer';

  const { data, isLoading } = useQuery({
    queryKey: ['returns', returnType],
    queryFn: () => returnsApi.getAll(returnType)
  });

  const approveMutation = useMutation({
    mutationFn: returnsApi.approve,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setSelectedReturn(null);
    }
  });

  const postMutation = useMutation({
    mutationFn: returnsApi.post,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setSelectedReturn(null);
    }
  });

  const settlementMutation = useMutation({
    mutationFn: (data: { id: string, payload: any }) => returnsApi.addSettlement(data.id, data.payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['returns'] });
      setShowSettlementModal(false);
      setSelectedReturn(null);
    },
    onError: (err: any) => {
      alert(err?.response?.data?.detail || "Failed to process settlement");
    }
  });

  const handleSettlementSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (selectedReturn) {
      settlementMutation.mutate({
        id: selectedReturn.id,
        payload: settlementForm
      });
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-foreground">{pageTitle}</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Manage your {returnType.toLowerCase().replace('_', ' ')}s.
          </p>
        </div>
        <Link to={`${isSupplyIn ? '/supply-in' : '/supply-out'}/returns/new`}>
          <Button>+ Create Return</Button>
        </Link>
      </div>

      <div className="bg-card rounded-xl shadow-sm border border overflow-hidden">
        <table className="min-w-full divide-y divide-border">
          <thead className="bg-muted/50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Return No</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{partyLabel}</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-center text-xs font-medium text-muted-foreground uppercase tracking-wider">Financial</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Amount</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-card divide-y divide-border">
            {isLoading ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">Loading returns...</td></tr>
            ) : data?.items.length === 0 ? (
              <tr><td colSpan={7} className="px-6 py-4 text-center text-sm text-muted-foreground">No returns found.</td></tr>
            ) : (
              data?.items.map((ret) => (
                <tr key={ret.id} className="hover:bg-muted/50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground">{ret.return_date}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground font-medium">{ret.return_number || 'DRAFT'}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-muted-foreground">{ret.party_id.substring(0,8)}...</td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${ret.status === 'DRAFT' ? 'bg-muted text-muted-foreground' : 
                        ret.status === 'APPROVED' ? 'bg-blue-100 text-blue-800' : 
                        ret.status === 'COMPLETED' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                      {ret.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-center">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-muted text-foreground">
                      {ret.financial_status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-foreground text-right font-bold">₹{ret.grand_total.toFixed(2)}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button onClick={() => setSelectedReturn(ret)} className="text-primary-600 hover:text-primary-900">View</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* View Modal */}
      {selectedReturn && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] flex flex-col">
            <div className="p-6 border-b flex justify-between items-center">
              <div>
                <h3 className="text-xl font-bold text-foreground">
                  {selectedReturn.return_number || 'Draft Return'}
                </h3>
                <p className="text-sm text-muted-foreground">Original Order: {selectedReturn.original_order_id.substring(0, 8)}...</p>
              </div>
              <button onClick={() => setSelectedReturn(null)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            
            <div className="p-6 overflow-y-auto flex-1">
              <table className="min-w-full divide-y divide-border border mb-6 text-sm">
                <thead className="bg-muted/50">
                  <tr>
                    <th className="px-4 py-2 text-left text-muted-foreground font-medium">Item</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Return Qty</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Rate</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">GST</th>
                    <th className="px-4 py-2 text-right text-muted-foreground font-medium">Total</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {selectedReturn.lines.map((line: any) => (
                    <tr key={line.id}>
                      <td className="px-4 py-2">
                        {line.item_name_snapshot}
                        <div className="text-xs text-muted-foreground">Condition: {line.condition}</div>
                      </td>
                      <td className="px-4 py-2 text-right font-medium text-red-600">
                        {line.return_quantity} {line.unit_snapshot}
                      </td>
                      <td className="px-4 py-2 text-right">₹{line.rate.toFixed(2)}</td>
                      <td className="px-4 py-2 text-right">{line.gst_rate}%</td>
                      <td className="px-4 py-2 text-right font-medium">₹{line.line_total.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="flex flex-col md:flex-row justify-between mt-6 pt-4 border-t gap-6">
                <div className="w-full md:w-1/2">
                  <h4 className="font-semibold text-foreground mb-2">Settlements</h4>
                  {selectedReturn.settlements.length > 0 ? (
                    <div className="space-y-2">
                      {selectedReturn.settlements.map((s: any) => (
                        <div key={s.id} className="bg-card border rounded p-3 text-sm flex justify-between items-center shadow-sm">
                          <div>
                            <div className="font-medium text-foreground">{s.settlement_type.replace(/_/g, ' ')}</div>
                            <div className="text-muted-foreground text-xs">{new Date(s.settlement_date).toLocaleDateString()} {s.reference_number ? `| Ref: ${s.reference_number}` : ''}</div>
                            {s.notes && <div className="text-muted-foreground text-xs italic">Note: {s.notes}</div>}
                          </div>
                          <div className="font-bold text-green-600">
                            ₹{s.amount.toFixed(2)}
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="text-sm text-muted-foreground italic">No settlements recorded yet.</div>
                  )}
                </div>
                
                <div className="w-full md:w-64 space-y-2 text-sm bg-muted p-4 rounded-lg self-start border">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Subtotal</span>
                    <span>₹{selectedReturn.subtotal.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between font-bold text-lg pt-2 border-t mt-2">
                    <span>Grand Total</span>
                    <span>₹{selectedReturn.grand_total.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-green-600 font-semibold pt-1">
                    <span>Settled</span>
                    <span>₹{selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0).toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between text-red-600 font-bold pt-2 border-t mt-2">
                    <span>Balance</span>
                    <span>₹{(selectedReturn.grand_total - selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0)).toFixed(2)}</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-6 border-t bg-muted flex justify-end space-x-3 rounded-b-lg">
              <Button variant="secondary" onClick={() => setSelectedReturn(null)}>Close</Button>
              {selectedReturn.status === 'DRAFT' && (
                <Button 
                  onClick={() => approveMutation.mutate(selectedReturn.id)}
                  isLoading={approveMutation.isPending}
                >
                  Approve Return
                </Button>
              )}
              {selectedReturn.status === 'APPROVED' && (
                <Button 
                  onClick={() => postMutation.mutate(selectedReturn.id)}
                  isLoading={postMutation.isPending}
                >
                  Post Return (Process)
                </Button>
              )}
              {selectedReturn.status === 'COMPLETED' && selectedReturn.financial_status !== 'REFUNDED' && (
                <Button 
                  onClick={() => {
                    setSettlementForm({
                      settlement_type: isSupplyIn ? 'ADJUST_PAYABLE' : 'ADJUST_RECEIVABLE',
                      amount: selectedReturn.grand_total - selectedReturn.settlements.reduce((sum: number, s: any) => sum + s.amount, 0),
                      reference_number: '',
                      notes: ''
                    });
                    setShowSettlementModal(true);
                  }}
                >
                  Process Settlement
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Settlement Modal */}
      {showSettlementModal && selectedReturn && (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50">
          <div className="bg-card rounded-lg shadow-xl max-w-md w-full">
            <div className="p-6 border-b flex justify-between items-center">
              <h3 className="text-xl font-bold text-foreground">Process Settlement</h3>
              <button onClick={() => setShowSettlementModal(false)} className="text-gray-400 hover:text-muted-foreground text-2xl font-bold">&times;</button>
            </div>
            <form onSubmit={handleSettlementSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-muted-foreground">Settlement Type</label>
                <select 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.settlement_type}
                  onChange={(e) => setSettlementForm({...settlementForm, settlement_type: e.target.value})}
                  required
                >
                  {isSupplyIn ? (
                    <>
                      <option value="ADJUST_PAYABLE">Adjust Payable (Reduce what we owe)</option>
                      <option value="SUPPLIER_REFUND">Supplier Refund (Cash/Bank received)</option>
                      <option value="SUPPLIER_CREDIT">Supplier Credit (Credit Note)</option>
                    </>
                  ) : (
                    <>
                      <option value="ADJUST_RECEIVABLE">Adjust Receivable (Reduce what they owe)</option>
                      <option value="CUSTOMER_REFUND">Customer Refund (Cash/Bank paid)</option>
                      <option value="CUSTOMER_CREDIT">Customer Credit (Credit Note)</option>
                    </>
                  )}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-muted-foreground">Amount (₹)</label>
                <input 
                  type="number" 
                  step="0.01"
                  min="0.01"
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.amount}
                  onChange={(e) => setSettlementForm({...settlementForm, amount: parseFloat(e.target.value)})}
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground">Reference Number</label>
                <input 
                  type="text" 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.reference_number}
                  onChange={(e) => setSettlementForm({...settlementForm, reference_number: e.target.value})}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-muted-foreground">Notes</label>
                <textarea 
                  className="mt-1 w-full rounded-md border-input shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  value={settlementForm.notes}
                  onChange={(e) => setSettlementForm({...settlementForm, notes: e.target.value})}
                  rows={2}
                />
              </div>

              <div className="flex justify-end space-x-3 pt-4">
                <Button type="button" variant="secondary" onClick={() => setShowSettlementModal(false)}>Cancel</Button>
                <Button type="submit" isLoading={settlementMutation.isPending}>Confirm Settlement</Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
```

```css
// File: frontend/src/index.css
@import "tailwindcss";

/* ── Enable class-based dark mode for Tailwind v4 ────────────────────────── */
@variant dark (&:where(.dark, .dark *));

/* ── shadcn/ui CSS variable tokens ───────────────────────────────────────── */
@layer base {
  :root {
    --background:         0 0% 100%;
    --foreground:         222.2 84% 4.9%;

    --card:               0 0% 100%;
    --card-foreground:    222.2 84% 4.9%;

    --popover:            0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;

    --primary:            222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;

    --secondary:          210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    --muted:              210 40% 96.1%;
    --muted-foreground:   215.4 16.3% 46.9%;

    --accent:             210 40% 96.1%;
    --accent-foreground:  222.2 47.4% 11.2%;

    --destructive:        0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    --border:             214.3 31.8% 91.4%;
    --input:              214.3 31.8% 91.4%;
    --ring:               222.2 84% 4.9%;

    --radius:             0.5rem;

    /* Sidebar */
    --sidebar:            0 0% 100%;
    --sidebar-foreground: 240 5.3% 26.1%;
    --sidebar-primary:    240 5.9% 10%;
    --sidebar-primary-foreground: 0 0% 98%;
    --sidebar-accent:     240 4.8% 95.9%;
    --sidebar-accent-foreground: 240 5.9% 10%;
    --sidebar-border:     220 13% 91%;
    --sidebar-ring:       217.2 91.2% 59.8%;
  }

  .dark {
    --background:         222.2 84% 4.9%;
    --foreground:         210 40% 98%;

    --card:               222.2 84% 4.9%;
    --card-foreground:    210 40% 98%;

    --popover:            222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary:            210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary:          217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted:              217.2 32.6% 17.5%;
    --muted-foreground:   215 20.2% 65.1%;

    --accent:             217.2 32.6% 17.5%;
    --accent-foreground:  210 40% 98%;

    --destructive:        0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border:             217.2 32.6% 17.5%;
    --input:              217.2 32.6% 17.5%;
    --ring:               212.7 26.8% 83.9%;

    /* Sidebar dark */
    --sidebar:            222.2 84% 4.9%;
    --sidebar-foreground: 210 40% 98%;
    --sidebar-primary:    224.3 76.3% 48%;
    --sidebar-primary-foreground: 0 0% 100%;
    --sidebar-accent:     217.2 32.6% 17.5%;
    --sidebar-accent-foreground: 210 40% 98%;
    --sidebar-border:     217.2 32.6% 17.5%;
    --sidebar-ring:       217.2 91.2% 59.8%;
  }
}

/* ── Map CSS vars to Tailwind v4 theme ───────────────────────────────────── */
@theme inline {
  --color-background:         hsl(var(--background));
  --color-foreground:         hsl(var(--foreground));
  --color-card:               hsl(var(--card));
  --color-card-foreground:    hsl(var(--card-foreground));
  --color-popover:            hsl(var(--popover));
  --color-popover-foreground: hsl(var(--popover-foreground));
  --color-primary:            hsl(var(--primary));
  --color-primary-foreground: hsl(var(--primary-foreground));
  --color-secondary:          hsl(var(--secondary));
  --color-secondary-foreground: hsl(var(--secondary-foreground));
  --color-muted:              hsl(var(--muted));
  --color-muted-foreground:   hsl(var(--muted-foreground));
  --color-accent:             hsl(var(--accent));
  --color-accent-foreground:  hsl(var(--accent-foreground));
  --color-destructive:        hsl(var(--destructive));
  --color-destructive-foreground: hsl(var(--destructive-foreground));
  --color-border:             hsl(var(--border));
  --color-input:              hsl(var(--input));
  --color-ring:               hsl(var(--ring));
  --color-sidebar:            hsl(var(--sidebar));
  --color-sidebar-foreground: hsl(var(--sidebar-foreground));
  --color-sidebar-primary:    hsl(var(--sidebar-primary));
  --color-sidebar-primary-foreground: hsl(var(--sidebar-primary-foreground));
  --color-sidebar-accent:     hsl(var(--sidebar-accent));
  --color-sidebar-accent-foreground: hsl(var(--sidebar-accent-foreground));
  --color-sidebar-border:     hsl(var(--sidebar-border));
  --color-sidebar-ring:       hsl(var(--sidebar-ring));
  --radius-sm:   calc(var(--radius) - 4px);
  --radius-md:   calc(var(--radius) - 2px);
  --radius-lg:   var(--radius);
  --radius-xl:   calc(var(--radius) + 4px);
}

/* ── Base reset ──────────────────────────────────────────────────────────── */
@layer base {
  * {
    border-color: hsl(var(--border));
    outline-color: hsl(var(--ring) / 0.5);
  }

  body {
    background-color: hsl(var(--background));
    color: hsl(var(--foreground));
    font-feature-settings: "rlig" 1, "calt" 1;
    -webkit-font-smoothing: antialiased;
  }
}

/* ── Transition for theme switching ─────────────────────────────────────── */
*, *::before, *::after {
  transition-property: background-color, border-color, color;
  transition-duration: 150ms;
  transition-timing-function: ease;
}
/* Don't animate transforms/sizes */
[data-slot="dialog-content"], [data-slot="select-content"] {
  transition: none;
}

/* ── System prefers-dark: auto-apply before JS loads ────────────────────── */
@media (prefers-color-scheme: dark) {
  html:not([data-theme="light"]) {
    color-scheme: dark;
  }
}
```

```typescript
// File: frontend/src/lib/gst/constants.ts
export const BANK_ACCOUNT_TYPES = [
  { value: 'CURRENT',     label: 'Current Account' },
  { value: 'SAVINGS',     label: 'Savings Account' },
  { value: 'CASH_CREDIT', label: 'Cash Credit Account' },
  { value: 'OVERDRAFT',   label: 'Overdraft Account' },
  { value: 'NRE',         label: 'NRE Account' },
  { value: 'NRO',         label: 'NRO Account' },
  { value: 'OTHER',       label: 'Other' },
] as const;

export type BankAccountTypeValue = typeof BANK_ACCOUNT_TYPES[number]['value'];

// Country code list removed — PhoneInput now uses libphonenumber-js
// getCountries() + getCountryCallingCode() for the full dynamic list.
```

```typescript
// File: frontend/src/lib/gst/index.ts
export * from './stateCodes';
export * from './validator';
export * from './constants';
```

```typescript
// File: frontend/src/lib/gst/stateCodes.ts
export interface GSTState {
  code: string;
  name: string;
  isUnionTerritory: boolean;
}

export const GST_STATE_CODES: Record<string, GSTState> = {
  "01": { code: "01", name: "Jammu and Kashmir", isUnionTerritory: false },
  "02": { code: "02", name: "Himachal Pradesh", isUnionTerritory: false },
  "03": { code: "03", name: "Punjab", isUnionTerritory: false },
  "04": { code: "04", name: "Chandigarh", isUnionTerritory: true },
  "05": { code: "05", name: "Uttarakhand", isUnionTerritory: false },
  "06": { code: "06", name: "Haryana", isUnionTerritory: false },
  "07": { code: "07", name: "Delhi", isUnionTerritory: true },
  "08": { code: "08", name: "Rajasthan", isUnionTerritory: false },
  "09": { code: "09", name: "Uttar Pradesh", isUnionTerritory: false },
  "10": { code: "10", name: "Bihar", isUnionTerritory: false },
  "11": { code: "11", name: "Sikkim", isUnionTerritory: false },
  "12": { code: "12", name: "Arunachal Pradesh", isUnionTerritory: false },
  "13": { code: "13", name: "Nagaland", isUnionTerritory: false },
  "14": { code: "14", name: "Manipur", isUnionTerritory: false },
  "15": { code: "15", name: "Mizoram", isUnionTerritory: false },
  "16": { code: "16", name: "Tripura", isUnionTerritory: false },
  "17": { code: "17", name: "Meghalaya", isUnionTerritory: false },
  "18": { code: "18", name: "Assam", isUnionTerritory: false },
  "19": { code: "19", name: "West Bengal", isUnionTerritory: false },
  "20": { code: "20", name: "Jharkhand", isUnionTerritory: false },
  "21": { code: "21", name: "Odisha", isUnionTerritory: false },
  "22": { code: "22", name: "Chhattisgarh", isUnionTerritory: false },
  "23": { code: "23", name: "Madhya Pradesh", isUnionTerritory: false },
  "24": { code: "24", name: "Gujarat", isUnionTerritory: false },
  "25": { code: "25", name: "Daman and Diu", isUnionTerritory: true },
  "26": { code: "26", name: "Dadra and Nagar Haveli and Daman and Diu", isUnionTerritory: true },
  "27": { code: "27", name: "Maharashtra", isUnionTerritory: false },
  "29": { code: "29", name: "Karnataka", isUnionTerritory: false },
  "30": { code: "30", name: "Goa", isUnionTerritory: false },
  "31": { code: "31", name: "Lakshadweep", isUnionTerritory: true },
  "32": { code: "32", name: "Kerala", isUnionTerritory: false },
  "33": { code: "33", name: "Tamil Nadu", isUnionTerritory: false },
  "34": { code: "34", name: "Puducherry", isUnionTerritory: true },
  "35": { code: "35", name: "Andaman and Nicobar Islands", isUnionTerritory: true },
  "36": { code: "36", name: "Telangana", isUnionTerritory: false },
  "37": { code: "37", name: "Andhra Pradesh", isUnionTerritory: false },
  "38": { code: "38", name: "Ladakh", isUnionTerritory: true },
  "97": { code: "97", name: "Other Territory", isUnionTerritory: true },
  "99": { code: "99", name: "Centre Jurisdiction", isUnionTerritory: true },
};

export function getStateByCode(code: string): GSTState | null {
  return GST_STATE_CODES[code] ?? null;
}

export function getAllStates(): GSTState[] {
  return Object.values(GST_STATE_CODES).sort((a, b) =>
    a.code.localeCompare(b.code)
  );
}
```

```typescript
// File: frontend/src/lib/gst/validator.ts
import { GST_STATE_CODES } from './stateCodes';

const GSTIN_REGEX = /^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$/;


export interface GSTINValidation {
  valid: boolean;
  validLength: boolean;
  validStructure: boolean;
  validStateCode: boolean;
  validChecksum: boolean;
  errors: string[];
  normalized: string;
}

export interface GSTINParseResult {
  gstin: string;
  stateCode: string;
  stateName: string | null;
  isUnionTerritory: boolean;
  pan: string;
  panHolderType: string;
  entityNumber: string;
  defaultCharacter: string;
  checkDigit: string;
}

function computeChecksum(gstin: string): string {
  const body = gstin.slice(0, 14);
  const vals = body.split('').map((c) =>
    c >= '0' && c <= '9' ? parseInt(c) : c.charCodeAt(0) - 55
  );
  const weighted = vals.map((v, i) => v * ((i % 2) + 1));
  const reduced = weighted.map((x) => Math.floor(x / 36) + (x % 36));
  const sum = reduced.reduce((a, b) => a + b, 0);
  const csum = 36 - (sum % 36);
  if (csum >= 36) return '0';
  return csum < 10 ? String(csum) : String.fromCharCode(csum + 55);
}

export function validateGSTIN(raw: string): GSTINValidation {
  const normalized = raw.toUpperCase().replace(/\s+/g, '');
  const errors: string[] = [];
  let validLength = false;
  let validStructure = false;
  let validStateCode = false;
  let validChecksum = false;

  if (normalized.length !== 15) {
    errors.push(`GSTIN must be exactly 15 characters (currently ${normalized.length})`);
  } else {
    validLength = true;
  }

  if (validLength) {
    if (!GSTIN_REGEX.test(normalized)) {
      errors.push('GSTIN format is invalid. Expected: SSAAAAANNNNAS(Z)D');
    } else {
      validStructure = true;
    }
  }

  if (validLength) {
    const stateCode = normalized.slice(0, 2);
    if (!GST_STATE_CODES[stateCode]) {
      errors.push(`Invalid state code: ${stateCode}`);
    } else {
      validStateCode = true;
    }
  }

  if (validLength) {
    const expected = computeChecksum(normalized);
    if (normalized[14] !== expected) {
      errors.push(`Invalid checksum digit. Expected: ${expected}`);
    } else {
      validChecksum = true;
    }
  }

  const valid = validLength && validStructure && validStateCode && validChecksum;

  return { valid, validLength, validStructure, validStateCode, validChecksum, errors, normalized };
}

export function parseGSTIN(raw: string): GSTINParseResult | null {
  const validation = validateGSTIN(raw);
  if (!validation.validLength) return null;
  const gstin = validation.normalized;
  const stateCode = gstin.slice(0, 2);
  const state = GST_STATE_CODES[stateCode] ?? null;
  return {
    gstin,
    stateCode,
    stateName: state?.name ?? null,
    isUnionTerritory: state?.isUnionTerritory ?? false,
    pan: gstin.slice(2, 12),
    panHolderType: gstin[11],
    entityNumber: gstin[12],
    defaultCharacter: gstin[13],
    checkDigit: gstin[14],
  };
}
```

```typescript
// File: frontend/src/lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

```tsx
// File: frontend/src/main.tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import './index.css'
import { AppProviders } from './app/providers'
import { router } from './app/router'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AppProviders>
      <RouterProvider router={router} />
    </AppProviders>
  </StrictMode>,
)
```

```javascript
// File: frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      }
    },
  },
  plugins: [],
}
```

```json
// File: frontend/tsconfig.app.json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.app.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023", "DOM"],
    "module": "esnext",
    "types": ["vite/client"],
    "allowArbitraryExtensions": true,
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
```

```json
// File: frontend/tsconfig.json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" }
  ]
}
```

```json
// File: frontend/tsconfig.node.json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.node.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023"],
    "types": ["node"],
    "skipLibCheck": true,

    /* Bundler mode */
    "module": "nodenext",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,

    /* Linting */
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "erasableSyntaxOnly": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["vite.config.ts"]
}
```

```typescript
// File: frontend/vite.config.ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    tailwindcss(),
    react(),
  ],
})
```
