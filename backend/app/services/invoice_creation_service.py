from sqlalchemy.orm import Session
from app.models.invoice import Invoice, InvoiceLine
from app.models.document_link import DocumentLink
import uuid
from datetime import datetime, timezone

def utc_now():
    return datetime.now(timezone.utc)

class InvoiceCreationService:
    def __init__(self, db: Session):
        self.db = db
        
    def _calculate_gst(self, items):
        # Implementation to centralize GST logic
        pass

    def create_from_order(self, order_id: str, company_id: str, created_by: str) -> Invoice:
        # Fetch supply order and validate
        # Then create draft invoice with proper origin links
        # Create DocumentLink record
        # Return draft invoice
        pass

    def convert_to_final(self, invoice_id: str):
        # BEGIN TRANSACTION logic
        # Assign series number
        # Set FINALIZED
        # COMMIT
        pass
