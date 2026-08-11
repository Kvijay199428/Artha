from sqlalchemy.orm import Session
from app.models.audit import AuditLog

class AuditService:
    @staticmethod
    def log(db: Session, company_id: str | None, entity_type: str, entity_id: str, 
            action: str, field_name: str = None, old_value: str = None, 
            new_value: str = None, reason: str = None, metadata: dict = None):
        log = AuditLog(
            company_id=company_id,
            entity_type=entity_type,
            entity_id=entity_id,
            action=action,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            reason=reason,
            metadata_json=metadata,
        )
        db.add(log)
        db.commit()
