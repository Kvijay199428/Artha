GSTIN_REGEX = r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
GSTN_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GSTIN_LENGTH = 15
PAN_TYPES = ["C", "P", "H", "F", "A", "T", "B", "L", "J", "G"]
BANK_ACCOUNT_TYPES = {
    "SAVINGS": "Savings Account",
    "CURRENT": "Current Account",
    "CASH_CREDIT": "Cash Credit Account",
    "OVERDRAFT": "Overdraft Account",
    "NRE": "NRE Account",
    "NRO": "NRO Account",
    "OTHER": "Other",
}
