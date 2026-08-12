```
// File: backend/.env.example
APP_ENV=development
DATABASE_URL=sqlite:///data/gst_billing.db
SECRET_KEY=change-this-to-a-secure-random-key-min-32-chars
SESSION_SECRET=another-secure-random-key
STORAGE_PATH=storage
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
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
from app.api.v1 import auth, company, units, items, parties, invoices, master

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(company.router)
api_router.include_router(units.router)
api_router.include_router(items.router)
api_router.include_router(parties.router)
api_router.include_router(invoices.router)
api_router.include_router(master.router)
```

```python
// File: backend/app/api/v1/auth.py
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
```

```python
// File: backend/app/api/v1/company.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.company import CompanyDetailResponse

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
        mobile=company.mobile,
        office_phone=company.office_phone,
        email=company.email,
        authorized_person_name=company.authorized_person_name,
        authorized_person_designation=company.authorized_person_designation,
        gst_details={
            "id": gst.id,
            "gstin": gst.gstin,
            "state_code": gst.state_code,
            "state_name": gst.state_name,
            "pan": gst.pan,
            "gstin_validation_status": gst.gstin_validation_status,
        } if gst else None,
        addresses=addresses,
        bank_accounts=banks,
        created_at=company.created_at,
        updated_at=company.updated_at,
    ))
```

```python
// File: backend/app/api/v1/invoices.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.dependencies.auth import get_current_company
from app.schemas.common import ApiResponse
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceListResponse, InvoiceFinalizeRequest, InvoiceCancelRequest
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/invoices", tags=["Invoices"])

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
    return ApiResponse(success=True, data=ItemResponse(
        id=item.id,
        company_id=item.company_id,
        item_type=item.item_type,
        item_name=item.item_name,
        sku_code=item.sku_code,
        unit_id=item.unit_id,
        unit_name=None,
        unit_symbol=None,
        hsn_sac_code=item.hsn_sac_code,
        gst_applicable=item.gst_applicable,
        gst_rate_id=item.default_gst_rate_id,
        gst_rate=None,
        description=item.description,
        status=item.status,
        created_at=item.created_at,
        updated_at=item.updated_at,
    ))

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
    cors_origins: str = "http://localhost:5173"
    
    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]
    
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
)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "error": {"code": exc.code, "message": exc.message, "fields": getattr(exc, "fields", None)}}
    )

app.include_router(api_router, prefix="/api")

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
    Invoice, InvoiceLine, InvoiceSeries, Payment,
    CreditNote, DebitNote
)
from app.models.audit import AuditLog
from app.models.master import GSTStateCode, GSTRate, HSNSACCode

__all__ = [
    "Base",
    "Company", "CompanyGSTDetail", "CompanyAddress", "CompanyContact",
    "CompanyBankAccount", "CompanyAsset", "CompanyAuth", "CompanySession",
    "Unit", "UnitAlias", "UnitVersion",
    "Item", "ItemVersion",
    "Party", "PartyAddress", "PartyBankAccount", "PartyLedgerEntry", "PaymentAllocation",
    "Invoice", "InvoiceLine", "InvoiceSeries", "Payment", "CreditNote", "DebitNote",
    "AuditLog",
    "GSTStateCode", "GSTRate", "HSNSACCode",
]
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
    
    mobile = Column(String(20), nullable=False)
    office_phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=False)
    website = Column(String(200), nullable=True)
    
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
    account_type = Column(String(20), default="Current")
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
    
    # Customer snapshots
    customer_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    customer_name_snapshot = Column(String(200), nullable=False)
    customer_gstin_snapshot = Column(String(15), nullable=True)
    customer_address_snapshot = Column(Text, nullable=True)
    customer_state_snapshot = Column(String(100), nullable=True)
    customer_state_code_snapshot = Column(String(2), nullable=True)
    place_of_supply = Column(String(100), nullable=False)
    
    # Seller snapshots
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

class CreditNote(Base):
    __tablename__ = "credit_notes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    credit_note_number = Column(String(50), nullable=False)
    original_invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    note_date = Column(DateTime, nullable=False)
    reason = Column(String(200), nullable=False)
    taxable_amount = Column(Numeric(15, 2), default=0)
    cgst = Column(Numeric(15, 2), default=0)
    sgst = Column(Numeric(15, 2), default=0)
    igst = Column(Numeric(15, 2), default=0)
    cess = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    status = Column(String(20), default="ACTIVE")
    created_at = Column(DateTime, default=utc_now)

class DebitNote(Base):
    __tablename__ = "debit_notes"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    debit_note_number = Column(String(50), nullable=False)
    original_invoice_id = Column(String(36), ForeignKey("invoices.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)
    note_date = Column(DateTime, nullable=False)
    reason = Column(String(200), nullable=False)
    taxable_amount = Column(Numeric(15, 2), default=0)
    cgst = Column(Numeric(15, 2), default=0)
    sgst = Column(Numeric(15, 2), default=0)
    igst = Column(Numeric(15, 2), default=0)
    cess = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    status = Column(String(20), default="ACTIVE")
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
    mobile = Column(String(20), nullable=True)
    alternate_mobile = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    website = Column(String(200), nullable=True)
    gstin = Column(String(15), nullable=True)
    gst_registration_type = Column(String(30), default="Regular")  # Regular, Composition, Unregistered, SEZ
    gstin_status = Column(String(20), default="Unknown")  # Active, Cancelled, Suspended
    pan = Column(String(10), nullable=True)
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

```
// File: backend/app/repositories/.gitkeep

```

```python
// File: backend/app/schemas/auth.py
from pydantic import BaseModel, Field

class CompanySetupRequest(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=200)
    ownership_type: str = Field(...)
    gst_registered: bool = True
    gstin: str | None = Field(None, max_length=15)
    address_line_1: str = Field(..., min_length=1, max_length=200)
    address_line_2: str | None = Field(None, max_length=200)
    city: str = Field(..., min_length=1, max_length=100)
    district: str | None = Field(None, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    state_code: str = Field(..., min_length=1, max_length=2)
    pincode: str = Field(..., min_length=4, max_length=10)
    country: str = Field(default="India")
    mobile: str = Field(..., min_length=10, max_length=20)
    office_phone: str | None = Field(None, max_length=20)
    email: str = Field(..., max_length=100)
    authorized_person_name: str = Field(..., min_length=1, max_length=100)
    authorized_person_designation: str | None = Field(None, max_length=100)
    bank_account_holder_name: str = Field(..., min_length=1, max_length=100)
    bank_account_number: str = Field(..., min_length=4, max_length=50)
    bank_ifsc: str = Field(..., min_length=11, max_length=20)
    bank_name: str | None = Field(None, max_length=100)
    bank_branch: str = Field(..., min_length=1, max_length=100)
    bank_account_type: str = Field(default="Current")
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
    legal_name: str | None
    ownership_type: str
    status: str
    mobile: str
    email: str
    authorized_person_name: str
    logo_url: str | None
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
    gstin_validation_status: str

class CompanyDetailResponse(BaseModel):
    id: str
    company_name: str
    legal_name: Optional[str]
    trade_name: Optional[str]
    ownership_type: str
    status: str
    mobile: str
    office_phone: Optional[str]
    email: str
    authorized_person_name: str
    authorized_person_designation: Optional[str]
    gst_details: Optional[CompanyGSTDetailSchema]
    addresses: list[CompanyAddressSchema]
    bank_accounts: list[CompanyBankAccountSchema]
    created_at: datetime
    updated_at: datetime
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
    upi_id: Optional[str] = Field(None, max_length=100)
    is_primary: bool = True

class PartyCreate(BaseModel):
    legal_name: str = Field(..., min_length=1, max_length=200)
    trade_name: Optional[str] = Field(None, max_length=200)
    party_type: str = Field(default="Proprietorship")
    account_type: str = Field(..., pattern="^(CUSTOMER|SUPPLIER|BOTH)$")
    contact_person: Optional[str] = Field(None, max_length=100)
    mobile: Optional[str] = Field(None, max_length=20)
    alternate_mobile: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=100)
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: str = Field(default="Regular")
    pan: Optional[str] = Field(None, max_length=10)
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
    mobile: Optional[str] = None
    email: Optional[str] = None
    gstin: Optional[str] = Field(None, max_length=15)
    gst_registration_type: Optional[str] = None
    pan: Optional[str] = Field(None, max_length=10)
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
    mobile: Optional[str]
    email: Optional[str]
    gstin: Optional[str]
    gst_registration_type: str
    pan: Optional[str]
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
```

```python
// File: backend/app/services/company_service.py
from sqlalchemy.orm import Session
from app.models.company import Company, CompanyGSTDetail, CompanyAddress, CompanyBankAccount, CompanyAuth
from app.schemas.auth import CompanySetupRequest
from app.core.security import hash_pin, generate_id
from app.core.exceptions import ValidationException, ConflictException
from app.utils.gstin import validate_gstin

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
            office_phone=data.office_phone,
            email=data.email,
            authorized_person_name=data.authorized_person_name,
            authorized_person_designation=data.authorized_person_designation,
        )
        db.add(company)
        db.flush()
        
        # GST details
        gst_detail = None
        if data.gst_registered and data.gstin:
            gst_validation = validate_gstin(data.gstin)
            if not gst_validation["valid"]:
                raise ValidationException("Invalid GSTIN. Please check the 15-character GST number.")
            
            gst_detail = CompanyGSTDetail(
                company_id=company.id,
                gstin=gst_validation["normalized"],
                state_code=gst_validation["state_code"],
                pan=gst_validation["pan"],
                registration_number=gst_validation["registration_number"],
                gstin_character_14=gst_validation["default_code"],
                checksum=gst_validation["checksum"],
                gstin_validation_status="VALID" if gst_validation["valid"] else "INVALID",
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
        
        # Bank account
        bank = CompanyBankAccount(
            company_id=company.id,
            account_holder_name=data.bank_account_holder_name,
            account_number=data.bank_account_number,
            ifsc=data.bank_ifsc.upper(),
            bank_name=data.bank_name,
            branch=data.bank_branch,
            account_type=data.bank_account_type,
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
    def save_company_logo(cls, company_id: str, upload: UploadFile) -> dict:
        """Save company logo to storage.
        
        Returns metadata dict with path, mime_type, size.
        """
        mime_type, size = cls._validate_image(upload)
        
        storage = cls._get_storage_path()
        logo_dir = storage / "company-logos" / company_id
        logo_dir.mkdir(parents=True, exist_ok=True)
        
        ext = mimetypes.guess_extension(mime_type) or ".png"
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"logo_{timestamp}{ext}"
        safe_name = cls._safe_filename(filename)
        
        file_path = logo_dir / safe_name
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        
        return {
            "file_path": str(file_path.relative_to(storage)),
            "mime_type": mime_type,
            "file_size": size,
            "filename": safe_name,
        }
    
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
        return item
    
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
        return item
    
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
        item = db.query(Item).filter(Item.id == item_id, Item.company_id == company_id).first()
        if not item:
            raise NotFoundException("Item not found")
        return item
```

```python
// File: backend/app/services/party_service.py
from sqlalchemy.orm import Session
from app.models.party import Party, PartyAddress, PartyBankAccount
from app.core.exceptions import NotFoundException, ValidationException
from app.services.audit_service import AuditService

class PartyService:
    @staticmethod
    def create_party(db: Session, company_id: str, data: dict) -> Party:
        party = Party(
            company_id=company_id,
            legal_name=data["legal_name"],
            trade_name=data.get("trade_name"),
            party_type=data.get("party_type", "Proprietorship"),
            account_type=data["account_type"],
            contact_person=data.get("contact_person"),
            mobile=data.get("mobile"),
            alternate_mobile=data.get("alternate_mobile"),
            email=data.get("email"),
            gstin=data.get("gstin"),
            gst_registration_type=data.get("gst_registration_type", "Regular"),
            pan=data.get("pan"),
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
        
        for field in ["legal_name", "trade_name", "party_type", "account_type", "contact_person",
                      "mobile", "email", "gstin", "gst_registration_type", "pan", "state", 
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

```
// File: backend/migrations/.gitkeep

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
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app*"]
```

```python
// File: backend/seed_data.py
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.master import GSTStateCode, GSTRate

def seed_gst_states(db: Session):
    if db.query(GSTStateCode).first():
        return
    states = [
        ("01", "Jammu and Kashmir", False),
        ("02", "Himachal Pradesh", False),
        ("03", "Punjab", False),
        ("04", "Chandigarh", True),
        ("05", "Uttarakhand", False),
```

```
// File: backend/tests/.gitkeep

```

```
// File: docs/.gitkeep

```

```
// File: frontend/public/.gitkeep

```

```
// File: frontend/src/api/.gitkeep

```

```
// File: frontend/src/app/.gitkeep

```

```
// File: frontend/src/components/common/.gitkeep

```

```
// File: frontend/src/components/forms/.gitkeep

```

```
// File: frontend/src/components/modals/.gitkeep

```

```
// File: frontend/src/components/tables/.gitkeep

```

```
// File: frontend/src/features/auth/.gitkeep

```

```
// File: frontend/src/features/company/.gitkeep

```

```
// File: frontend/src/features/customers/.gitkeep

```

```
// File: frontend/src/features/invoices/.gitkeep

```

```
// File: frontend/src/features/items/.gitkeep

```

```
// File: frontend/src/features/units/.gitkeep

```

```
// File: frontend/src/hooks/.gitkeep

```

```
// File: frontend/src/stores/.gitkeep

```

```
// File: frontend/src/types/.gitkeep

```

```
// File: frontend/src/utils/.gitkeep

```
