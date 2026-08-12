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

    @staticmethod
    def list_categories(db: Session):
        return db.query(UnitCategory).filter(UnitCategory.status == "ACTIVE").order_by(UnitCategory.name).all()

    @staticmethod
    def update_unit(db: Session, company_id: str, unit_id: str, data: dict) -> Unit:
        unit = UnitService.get_unit(db, unit_id, company_id)
        if unit.is_predefined:
            raise ValidationException("Cannot modify predefined units")
        
        formula = data.get("conversion_formula")
        if formula:
            UnitService._validate_formula(formula)
        
        for key, value in data.items():
            if hasattr(unit, key) and value is not None:
                if key == "symbol":
                    setattr(unit, key, value.upper())
                else:
                    setattr(unit, key, value)
        
        db.commit()
        db.refresh(unit)
        AuditService.log(db, company_id, "UNIT", unit.id, "UPDATED")
        return unit
    
    @staticmethod
    def delete_unit(db: Session, company_id: str, unit_id: str):
        unit = UnitService.get_unit(db, unit_id, company_id)
        if unit.is_predefined:
            raise ValidationException("Cannot delete predefined units")
            
        from app.models.item import Item
        # In actual implementation check for usage in invoice_lines as well
        in_use = db.query(Item).filter(Item.unit_id == unit_id).first()
        if in_use:
            unit.is_active = False
            db.commit()
            AuditService.log(db, company_id, "UNIT", unit.id, "DEACTIVATED")
        else:
            db.delete(unit)
            db.commit()
            AuditService.log(db, company_id, "UNIT", unit_id, "DELETED")
