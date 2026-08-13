from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Enum, Text, Integer
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.audit import AuditableMixin

class OrderType(str, enum.Enum):
    PURCHASE = "PURCHASE"
    SALES = "SALES"

class TaxTreatment(str, enum.Enum):
    GST = "GST"
    WITHOUT_GST = "WITHOUT_GST"

class OrderStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    CONFIRMED = "CONFIRMED"
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"
    FULFILLED = "FULFILLED"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class SupplyOrder(Base, AuditableMixin):
    __tablename__ = "supply_orders"

    id = Column(String(36), primary_key=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    party_id = Column(String(36), ForeignKey("parties.id"), nullable=False)

    order_type = Column(Enum(OrderType), nullable=False)
    tax_treatment = Column(Enum(TaxTreatment), nullable=False)
    order_number = Column(String(50), nullable=True, index=True)
    
    order_date = Column(Date, nullable=False)
    expected_date = Column(Date, nullable=True)
    
    place_of_supply = Column(String(2), nullable=True) # State code
    
    status = Column(Enum(OrderStatus), default=OrderStatus.DRAFT, nullable=False)
    revision = Column(Integer, default=1, nullable=False)

    subtotal = Column(Numeric(15, 2), default=0)
    discount_total = Column(Numeric(15, 2), default=0)
    taxable_total = Column(Numeric(15, 2), default=0)
    
    cgst_total = Column(Numeric(15, 2), default=0)
    sgst_total = Column(Numeric(15, 2), default=0)
    igst_total = Column(Numeric(15, 2), default=0)
    cess_total = Column(Numeric(15, 2), default=0)
    
    other_charges = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(15, 2), default=0)
    grand_total = Column(Numeric(15, 2), default=0)
    amount_in_words = Column(String(255), nullable=True)

    notes = Column(Text, nullable=True)
    terms = Column(Text, nullable=True)

    lines = relationship("SupplyOrderLine", back_populates="order", cascade="all, delete-orphan")
    party = relationship("Party")


class SupplyOrderLine(Base):
    __tablename__ = "supply_order_lines"

    id = Column(String(36), primary_key=True)
    order_id = Column(String(36), ForeignKey("supply_orders.id", ondelete="CASCADE"), nullable=False)
    item_id = Column(String(36), ForeignKey("items.id"), nullable=True)

    # Snapshots
    item_name_snapshot = Column(String(255), nullable=False)
    sku_snapshot = Column(String(100), nullable=True)
    hsn_sac_snapshot = Column(String(20), nullable=True)
    
    unit_id = Column(String(36), nullable=False)
    unit_name_snapshot = Column(String(100), nullable=False)
    unit_symbol_snapshot = Column(String(20), nullable=False)
    
    quantity = Column(Numeric(15, 4), nullable=False)
    fulfilled_quantity = Column(Numeric(15, 4), default=0, nullable=False)
    
    rate = Column(Numeric(15, 2), nullable=False)
    
    discount_type = Column(String(20), default="NONE") # NONE, PERCENT, FIXED
    discount_value = Column(Numeric(15, 2), default=0)
    
    tax_treatment = Column(Enum(TaxTreatment), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0)
    
    taxable_value = Column(Numeric(15, 2), default=0)
    cgst_amount = Column(Numeric(15, 2), default=0)
    sgst_amount = Column(Numeric(15, 2), default=0)
    igst_amount = Column(Numeric(15, 2), default=0)
    cess_amount = Column(Numeric(15, 2), default=0)
    
    line_total = Column(Numeric(15, 2), nullable=False)
    description = Column(Text, nullable=True)

    order = relationship("SupplyOrder", back_populates="lines")
