class AppException(Exception):
    def __init__(self, status_code, error_code, message, details: dict | None = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}

        super().__init__(message)

    