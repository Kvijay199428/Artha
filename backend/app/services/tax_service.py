"""GST Tax Calculation Engine.
Determines applicable tax treatment based on transaction rules.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any
from app.models.company import CompanyGSTDetail
from app.models.party import Party

class TaxService:
    """Authoritative tax calculation service.
    
    Rules applied:
    - Intra-state (seller state == place of supply): CGST + SGST/UTGST
    - Inter-state (seller state != place of supply): IGST
    - GST rate is snapshotted from item master at transaction time
    """
    
    @staticmethod
    def determine_tax_treatment(
        seller_state_code: str,
        customer_state_code: str,
        place_of_supply_state_code: str,
        customer_gstin: str | None = None,
    ) -> Dict[str, Any]:
        """Determine tax treatment for a transaction.
        
        Returns dict with:
            - is_interstate: bool
            - cgst_applicable: bool
            - sgst_applicable: bool
            - igst_applicable: bool
            - tax_split_ratio: dict (for dividing tax into components)
        """
        # Use place of supply as the determining factor for destination-based GST
        pos_code = place_of_supply_state_code or customer_state_code
        seller = seller_state_code or ""
        
        is_interstate = seller != pos_code
        
        # Unregistered customers may still attract IGST if inter-state
        # SEZ, Export, Composition etc. would extend here in future
        
        return {
            "is_interstate": is_interstate,
            "cgst_applicable": not is_interstate,
            "sgst_applicable": not is_interstate,
            "igst_applicable": is_interstate,
            "tax_split_ratio": {
                "cgst": Decimal("0.5"),
                "sgst": Decimal("0.5"),
                "igst": Decimal("1.0"),
            } if not is_interstate else {
                "cgst": Decimal("0"),
                "sgst": Decimal("0"),
                "igst": Decimal("1.0"),
            }
        }
    
    @staticmethod
    def calculate_line_tax(
        taxable_value: Decimal,
        gst_rate: Decimal,
        treatment: Dict[str, Any],
        precision: int = 2
    ) -> Dict[str, Decimal]:
        """Calculate tax components for a single line.
        
        Returns:
            {
                "cgst_rate": Decimal,
                "sgst_rate": Decimal,
                "igst_rate": Decimal,
                "cgst_amount": Decimal,
                "sgst_amount": Decimal,
                "igst_amount": Decimal,
                "total_tax": Decimal,
            }
        """
        quantize = Decimal("0.01")
        
        if treatment["is_interstate"]:
            cgst_rate = Decimal("0")
            sgst_rate = Decimal("0")
            igst_rate = gst_rate
            igst_amount = (taxable_value * igst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            cgst_amount = Decimal("0")
            sgst_amount = Decimal("0")
        else:
            half_rate = (gst_rate / 2).quantize(quantize, rounding=ROUND_HALF_UP)
            cgst_rate = half_rate
            sgst_rate = half_rate
            igst_rate = Decimal("0")
            cgst_amount = (taxable_value * cgst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            sgst_amount = (taxable_value * sgst_rate / 100).quantize(quantize, rounding=ROUND_HALF_UP)
            igst_amount = Decimal("0")
        
        return {
            "cgst_rate": cgst_rate,
            "sgst_rate": sgst_rate,
            "igst_rate": igst_rate,
            "cgst_amount": cgst_amount,
            "sgst_amount": sgst_amount,
            "igst_amount": igst_amount,
            "total_tax": cgst_amount + sgst_amount + igst_amount,
        }
    
    @staticmethod
    def calculate_invoice_totals(lines: list[Dict[str, Any]]) -> Dict[str, Decimal]:
        """Aggregate totals from calculated lines.
        
        Input lines should have: taxable_value, cgst_amount, sgst_amount, igst_amount, line_total
        """
        quantize = Decimal("0.01")
        totals = {
            "subtotal": Decimal("0"),
            "discount_total": Decimal("0"),
            "taxable_total": Decimal("0"),
            "cgst_total": Decimal("0"),
            "sgst_total": Decimal("0"),
            "igst_total": Decimal("0"),
            "grand_total": Decimal("0"),
        }
        for line in lines:
            totals["subtotal"] += Decimal(str(line.get("gross", 0)))
            totals["discount_total"] += Decimal(str(line.get("discount_amount", 0)))
            totals["taxable_total"] += Decimal(str(line.get("taxable_value", 0)))
            totals["cgst_total"] += Decimal(str(line.get("cgst_amount", 0)))
            totals["sgst_total"] += Decimal(str(line.get("sgst_amount", 0)))
            totals["igst_total"] += Decimal(str(line.get("igst_amount", 0)))
            totals["grand_total"] += Decimal(str(line.get("line_total", 0)))
        
        return {k: v.quantize(quantize, rounding=ROUND_HALF_UP) for k, v in totals.items()}