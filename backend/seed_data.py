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
       
