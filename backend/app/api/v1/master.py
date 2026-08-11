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
