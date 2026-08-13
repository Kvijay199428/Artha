class GSTINValidationError(Exception):
    def __init__(self, message: str, code: str = "VALIDATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)

class InvalidGSTINLength(GSTINValidationError):
    def __init__(self, message: str = "GSTIN must be exactly 15 characters long"):
        super().__init__(message, "INVALID_LENGTH")

class InvalidGSTINFormat(GSTINValidationError):
    def __init__(self, message: str = "Invalid GSTIN format"):
        super().__init__(message, "INVALID_FORMAT")

class InvalidGSTINChecksum(GSTINValidationError):
    def __init__(self, message: str = "Invalid GSTIN checksum"):
        super().__init__(message, "INVALID_CHECKSUM")

class InvalidGSTStateCode(GSTINValidationError):
    def __init__(self, message: str = "Invalid GST state code"):
        super().__init__(message, "INVALID_STATE_CODE")
