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