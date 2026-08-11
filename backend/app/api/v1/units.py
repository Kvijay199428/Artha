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

