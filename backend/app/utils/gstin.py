import re

GSTIN_REGEX = re.compile(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$")
GSTN_CODEPOINT_CHARS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def validate_gstin_format(gstin: str) -> bool:
    """Validate GSTIN format using regex."""
    if not gstin or len(gstin) != 15:
        return False
    return bool(GSTIN_REGEX.match(gstin.upper()))

def validate_gstin_checksum(gstin: str) -> bool:
    """Validate GSTIN checksum using the official algorithm."""
    gstin = gstin.upper()
    if len(gstin) != 15:
        return False
    check = gstin[-1]
    body = gstin[:-1]
    # Convert each char to numeric value: 0-9 -> 0-9, A-Z -> 10-35
    l = [int(c) if c.isdigit() else ord(c) - 55 for c in body]
    # Apply alternating weights (2,1,2,1... from left to right, or equivalently index%2+1)
    l = [val * (ind % 2 + 1) for (ind, val) in enumerate(l)]
    # For each weighted value: digit = (digit // 36) + (digit % 36)
    l = [(x // 36) + (x % 36) for x in l]
    csum = 36 - (sum(l) % 36)
    csum = str(csum) if csum < 10 else chr(csum + 55)
    return check == csum

def validate_gstin(gstin: str) -> dict:
    """Full GSTIN validation with component extraction."""
    normalized = gstin.upper().strip().replace(" ", "")
    result = {
        "normalized": normalized,
        "valid_format": False,
        "valid_checksum": False,
        "valid": False,
        "state_code": None,
        "pan": None,
        "registration_number": None,
        "default_code": None,
        "checksum": None,
    }
    if len(normalized) != 15:
        return result
    result["valid_format"] = validate_gstin_format(normalized)
    result["valid_checksum"] = validate_gstin_checksum(normalized)
    result["valid"] = result["valid_format"] and result["valid_checksum"]
    result["state_code"] = normalized[:2]
    result["pan"] = normalized[2:12]
    result["registration_number"] = normalized[12]
    result["default_code"] = normalized[13]
    result["checksum"] = normalized[14]
    return result

def extract_pan_from_gstin(gstin: str) -> str:
    """Extract PAN from GSTIN."""
    normalized = gstin.upper().strip().replace(" ", "")
    if len(normalized) >= 12:
        return normalized[2:12]
    return ""