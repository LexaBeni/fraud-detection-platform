class AppException(Exception):
    def __init__(self, status_code, error_code, message, details: dict | None = None):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details or {}

        super().__init__(message)

class UserAlreadyExists(AppException):
    def __init__(self, information):
        self.information = information

        super().__init__(status_code=409, error_code="USER_ALREADY_EXISTS" , message=f"User with {self.information} already exists", details=self.information)

class InvalidCredentials(AppException):

    def __init__(self):

        super().__init__(status_code=401, error_code="INVALID_CREDENTIALS", message="Invalid email or password")

class PredictionNotFound(AppException):
    def __init__(self, id):
        self.id = id

        super().__init__(status_code=404, error_code="PREDICTION_NOT_FOUND", message=f"Prediction with id {id} is not found", details=id)

class InvalidRefreshToken(AppException):
    def __init__(self):
        
        super().__init__(status_code=401, error_code="INVALID_REFRESH_TOKEN", message="Invalid or expired refresh token.")

    