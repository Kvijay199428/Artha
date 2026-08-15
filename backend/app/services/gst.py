from decimal import Decimal

class GSTCalculationService:
    @staticmethod
    def determine_supply_type(company_state: str, place_of_supply: str) -> str:
        return "INTRA_STATE" if company_state == place_of_supply else "INTER_STATE"
        
    @staticmethod
    def calculate_tax(taxable_value: Decimal, gst_rate: Decimal, supply_type: str) -> dict:
        tax_amount = taxable_value * (gst_rate / Decimal('100'))
        if supply_type == "INTRA_STATE":
            half_tax = tax_amount / Decimal('2')
            return {
                "cgst": half_tax,
                "sgst": half_tax,
                "igst": Decimal('0'),
                "cess": Decimal('0')
            }
        else:
            return {
                "cgst": Decimal('0'),
                "sgst": Decimal('0'),
                "igst": tax_amount,
                "cess": Decimal('0')
            }
