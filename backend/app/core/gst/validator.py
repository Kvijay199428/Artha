import re
from .constants import GSTIN_REGEX, GSTN_CHARSET, GSTIN_LENGTH
from .state_codes import GSTStateMaster
from .parser import GSTINParser

class GSTINValidator:
    @staticmethod
    def validate_length(gstin: str) -> bool:
        return len(gstin.strip()) == GSTIN_LENGTH

    @staticmethod
    def validate_structure(gstin: str) -> bool:
        return bool(re.match(GSTIN_REGEX, gstin.strip().upper()))

    @staticmethod
    def validate_state_code(gstin: str) -> bool:
        code = GSTINParser.extract_state_code(gstin)
        return GSTStateMaster.is_valid_state_code(code)

    @staticmethod
    def validate_checksum(gstin: str) -> bool:
        gstin = gstin.strip().upper()
        if len(gstin) != 15:
            return False
        
        factor = 1
        sum_val = 0
        for i in range(14):
            char = gstin[i]
            if char not in GSTN_CHARSET:
                return False
            
            val = GSTN_CHARSET.index(char)
            val = val * factor
            factor = 2 if factor == 1 else 1
            
            val = (val // 36) + (val % 36)
            sum_val += val
            
        rem = sum_val % 36
        check_digit = GSTN_CHARSET[(36 - rem) % 36]
        
        return gstin[14] == check_digit

    @staticmethod
    def validate(gstin: str) -> dict:
        normalized = gstin.strip().upper()
        valid_len = GSTINValidator.validate_length(normalized)
        valid_struct = GSTINValidator.validate_structure(normalized)
        valid_state = GSTINValidator.validate_state_code(normalized)
        valid_check = GSTINValidator.validate_checksum(normalized)
        
        errors = []
        if not valid_len:
            errors.append("Invalid length")
        if not valid_struct:
            errors.append("Invalid structure")
        if not valid_state:
            errors.append("Invalid state code")
        if valid_len and valid_struct and not valid_check:
            errors.append("Invalid checksum")
            
        valid = valid_len and valid_struct and valid_state and valid_check
        
        if valid:
            level = "VALID"
        elif valid_struct and valid_state:
            level = "STRUCTURAL"
        else:
            level = "INVALID"
            
        return {
            "gstin": normalized,
            "valid": valid,
            "valid_length": valid_len,
            "valid_structure": valid_struct,
            "valid_state_code": valid_state,
            "valid_checksum": valid_check,
            "errors": errors,
            "level": level
        }
