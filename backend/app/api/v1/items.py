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
