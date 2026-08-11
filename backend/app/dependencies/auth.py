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
