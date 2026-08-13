from .schemas import GSTINValidationResult, GSTINParseResult, GSTStateResponse
from .validator import GSTINValidator
from .parser import GSTINParser
from .state_codes import GSTStateMaster

class GSTService:
    @staticmethod
    def validate(gstin: str) -> GSTINValidationResult:
        result = GSTINValidator.validate(gstin)
        parsed = None
        if result["valid_length"] and result["valid_structure"]:
            parsed_dict = GSTINParser.parse(result["gstin"])
            parsed = GSTINParseResult(
                gstin=parsed_dict["normalized"],
                state_code=parsed_dict["state_code"],
                state=parsed_dict["state"],
                is_union_territory=parsed_dict["is_union_territory"],
                pan=parsed_dict["pan"],
                pan_holder_type=parsed_dict["pan_holder_type"],
                entity_number=parsed_dict["entity_number"],
                default_character=parsed_dict["default_character"],
                check_digit=parsed_dict["check_digit"]
            )
            
        return GSTINValidationResult(
            gstin=result["gstin"],
            valid=result["valid"],
            valid_length=result["valid_length"],
            valid_structure=result["valid_structure"],
            valid_state_code=result["valid_state_code"],
            valid_checksum=result["valid_checksum"],
            errors=result["errors"],
            parsed=parsed,
            level=result["level"]
        )

    @staticmethod
    def parse(gstin: str) -> GSTINParseResult:
        parsed_dict = GSTINParser.parse(gstin)
        return GSTINParseResult(
            gstin=parsed_dict["normalized"],
            state_code=parsed_dict["state_code"],
            state=parsed_dict["state"],
            is_union_territory=parsed_dict["is_union_territory"],
            pan=parsed_dict["pan"],
            pan_holder_type=parsed_dict["pan_holder_type"],
            entity_number=parsed_dict["entity_number"],
            default_character=parsed_dict["default_character"],
            check_digit=parsed_dict["check_digit"]
        )

    @staticmethod
    def get_state(gstin: str) -> GSTStateResponse | None:
        code = GSTINParser.extract_state_code(gstin)
        state_data = GSTStateMaster.get_state(code)
        if state_data:
            return GSTStateResponse(**state_data)
        return None

    @staticmethod
    def extract_pan(gstin: str) -> str:
        return GSTINParser.extract_pan(gstin)

    @staticmethod
    def normalize(gstin: str) -> str:
        return gstin.strip().upper()
