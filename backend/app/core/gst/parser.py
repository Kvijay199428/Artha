from .state_codes import GSTStateMaster

class GSTINParser:
    @staticmethod
    def parse(gstin: str) -> dict:
        normalized = gstin.strip().upper()
        state_code = normalized[:2] if len(normalized) >= 2 else ""
        state_info = GSTStateMaster.get_state(state_code)
        
        return {
            "raw": gstin,
            "normalized": normalized,
            "state_code": state_code,
            "state": state_info["name"] if state_info else None,
            "is_union_territory": state_info["is_union_territory"] if state_info else False,
            "pan": normalized[2:12] if len(normalized) >= 12 else "",
            "pan_holder_type": normalized[11] if len(normalized) >= 12 else "",
            "entity_number": normalized[12] if len(normalized) >= 13 else "",
            "default_character": normalized[13] if len(normalized) >= 14 else "",
            "check_digit": normalized[14] if len(normalized) == 15 else "",
        }

    @staticmethod
    def extract_state_code(gstin: str) -> str:
        return gstin.strip().upper()[:2]

    @staticmethod
    def extract_state(gstin: str) -> str | None:
        return GSTStateMaster.get_state_name(GSTINParser.extract_state_code(gstin))

    @staticmethod
    def extract_pan(gstin: str) -> str:
        return gstin.strip().upper()[2:12]

    @staticmethod
    def extract_entity_number(gstin: str) -> str:
        return gstin.strip().upper()[12:13]
