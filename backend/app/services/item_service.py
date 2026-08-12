from sqlalchemy.orm import Session
from app.models.item import Item, ItemVersion
from app.models.unit import Unit
from app.core.exceptions import ValidationException, NotFoundException, ConflictException
from app.services.audit_service import AuditService

class ItemService:
    @staticmethod
    def create_item(db: Session, company_id: str, data: dict) -> Item:
        # Check SKU uniqueness
        if data.get("sku_code"):
            existing = db.query(Item).filter(
                Item.company_id == company_id,
                Item.sku_code.ilike(data["sku_code"].strip())
            ).first()
            if existing:
                raise ConflictException("SKU code already exists for this company")
        
        item = Item(
            company_id=company_id,
            item_type=data["item_type"],
            item_name=data["item_name"].strip(),
            sku_code=data.get("sku_code"),
            unit_id=data["unit_id"],
            hsn_sac_code=data.get("hsn_sac_code"),
            gst_applicable=data.get("gst_applicable", True),
            default_gst_rate_id=data.get("gst_rate_id"),
            description=data.get("description"),
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        AuditService.log(db, company_id, "ITEM", item.id, "CREATED")
        return ItemService.get_item(db, company_id, item.id)
    
    @staticmethod
    def update_item(db: Session, company_id: str, item_id: str, data: dict) -> Item:
        item = db.query(Item).filter(Item.id == item_id, Item.company_id == company_id).first()
        if not item:
            raise NotFoundException("Item not found")
        
        # Check SKU uniqueness if changing
        if data.get("sku_code") and data["sku_code"] != item.sku_code:
            existing = db.query(Item).filter(
                Item.company_id == company_id,
                Item.sku_code.ilike(data["sku_code"].strip()),
                Item.id != item_id
            ).first()
            if existing:
                raise ConflictException("SKU code already exists")
        
        # Track changes for audit
        changes = []
        for field in ["item_name", "sku_code", "unit_id", "hsn_sac_code", "gst_applicable", "default_gst_rate_id", "description", "status"]:
            if field in data and getattr(item, field) != data[field]:
                changes.append(f"{field}: {getattr(item, field)} -> {data[field]}")
                setattr(item, field, data[field])
        
        item.version += 1
        db.commit()
        db.refresh(item)
        
        if changes:
            AuditService.log(db, company_id, "ITEM", item.id, "UPDATED", reason="; ".join(changes))
        return ItemService.get_item(db, company_id, item.id)
    
    @staticmethod
    def list_items(db: Session, company_id: str, search: str = None):
        query = db.query(Item, Unit).outerjoin(Unit, Item.unit_id == Unit.id).filter(
            Item.company_id == company_id
        )
        if search:
            query = query.filter(
                Item.item_name.ilike(f"%{search}%") | 
                Item.sku_code.ilike(f"%{search}%")
            )
        results = query.order_by(Item.item_name).all()
        items = []
        for item, unit in results:
            d = {
                "id": item.id,
                "company_id": item.company_id,
                "item_type": item.item_type,
                "item_name": item.item_name,
                "sku_code": item.sku_code,
                "unit_id": item.unit_id,
                "unit_name": unit.unit_name if unit else None,
                "unit_symbol": unit.symbol if unit else None,
                "hsn_sac_code": item.hsn_sac_code,
                "gst_applicable": item.gst_applicable,
                "gst_rate_id": item.default_gst_rate_id,
                "gst_rate": None,
                "description": item.description,
                "status": item.status,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            items.append(d)
        return items
    
    @staticmethod
    def get_item(db: Session, company_id: str, item_id: str):
        from app.models.master import GSTRate
        result = db.query(Item, Unit, GSTRate).outerjoin(Unit, Item.unit_id == Unit.id).outerjoin(GSTRate, Item.default_gst_rate_id == GSTRate.id).filter(
            Item.id == item_id, Item.company_id == company_id
        ).first()
        if not result:
            raise NotFoundException("Item not found")
            
        item, unit, gst_rate = result
        return {
            "id": item.id,
            "company_id": item.company_id,
            "item_type": item.item_type,
            "item_name": item.item_name,
            "sku_code": item.sku_code,
            "unit_id": item.unit_id,
            "unit_name": unit.unit_name if unit else None,
            "unit_symbol": unit.symbol if unit else None,
            "hsn_sac_code": item.hsn_sac_code,
            "gst_applicable": item.gst_applicable,
            "gst_rate_id": item.default_gst_rate_id,
            "gst_rate": float(gst_rate.rate) if gst_rate else None,
            "description": item.description,
            "status": item.status,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }

    @staticmethod
    def delete_item(db: Session, company_id: str, item_id: str):
        item = db.query(Item).filter(Item.id == item_id, Item.company_id == company_id).first()
        if not item:
            raise NotFoundException("Item not found")
        
        # Check if used in invoices
        from app.models.invoice import InvoiceLine
        in_use = db.query(InvoiceLine).filter(InvoiceLine.item_id == item_id).first()
        if in_use:
            item.status = 'ARCHIVED'
            db.commit()
            AuditService.log(db, company_id, "ITEM", item.id, "ARCHIVED")
        else:
            db.delete(item)
            db.commit()
            AuditService.log(db, company_id, "ITEM", item.id, "DELETED")
