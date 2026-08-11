class AppException(Exception):
    def __init__(self, code: str, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundException(AppException):
    def __init__(self, message: str = "Not found"):
        super().__init__("NOT_FOUND", message, 404)

class ValidationException(AppException):
    def __init__(self, message: str = "Validation error", fields: dict = None):
        super().__init__("VALIDATION_ERROR", message, 422)
        self.fields = fields or {}

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__("CONFLICT", message, 409)

class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__("PERMISSION_DENIED", message, 403)

class AuthenticationException(AppException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__("AUTHENTICATION_REQUIRED", message, 401)

class InvoiceLockedException(AppException):
    def __init__(self, message: str = "Invoice is finalized and cannot be edited"):
        super().__init__("INVOICE_LOCKED", message, 409)