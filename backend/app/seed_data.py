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
