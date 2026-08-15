from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
# Use models and schemas

router = APIRouter()

@router.get("/search")
def search_documents(q: str, db: Session = Depends(deps.get_db)):
    # Search logic across invoices, notes, quotes, etc. based on `q`
    return {"results": []}
