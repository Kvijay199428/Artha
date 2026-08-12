"""Atomic invoice numbering service.
Ensures unique, sequential invoice numbers within a series.
"""
from sqlalchemy.orm import Session
from app.models.invoice import InvoiceSeries
from app.core.exceptions import ValidationException

class InvoiceNumberService:
    """Handles atomic invoice number assignment using row-level locking."""
    
    @staticmethod
    def get_or_create_series(
        db: Session,
        company_id: str,
        document_type: str = "TAX_INVOICE",
        prefix: str = "INV-",
        fiscal_year: str | None = None,
    ) -> InvoiceSeries:
        series = db.query(InvoiceSeries).filter(
            InvoiceSeries.company_id == company_id,
            InvoiceSeries.document_type == document_type,
            InvoiceSeries.prefix == prefix,
            InvoiceSeries.status == "ACTIVE",
        ).first()
        
        if not series:
            series = InvoiceSeries(
                company_id=company_id,
                document_type=document_type,
                prefix=prefix,
                starting_number=1,
                current_number=1,
                fiscal_year=fiscal_year,
            )
            db.add(series)
            db.flush()
        return series
    
    @staticmethod
    def assign_number(db: Session, series: InvoiceSeries) -> str:
        """Atomically assign next invoice number.
        
        Uses SELECT FOR UPDATE to prevent duplicate numbers under concurrency.
        """
        # Re-fetch with lock
        locked_series = db.query(InvoiceSeries).filter(
            InvoiceSeries.id == series.id
        ).with_for_update().first()
        
        if not locked_series:
            raise ValidationException("Invoice series not found")
        
        number = f"{locked_series.prefix}{locked_series.current_number:06d}"
        locked_series.current_number += 1
        return number