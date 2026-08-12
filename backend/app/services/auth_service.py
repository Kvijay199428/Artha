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
