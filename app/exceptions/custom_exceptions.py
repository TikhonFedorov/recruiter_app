class BaseAppException(Exception):
    """Базовое исключение для приложения"""
    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

class ValidationError(BaseAppException):
    """Исключение для ошибок валидации"""
    def __init__(self, message):
        super().__init__(message, 400)

class APIError(BaseAppException):
    """Исключение для ошибок API"""
    def __init__(self, message, status_code=500):
        super().__init__(message, status_code)

class RateLimitExceeded(BaseAppException):
    """Исключение для превышения лимитов"""
    def __init__(self, message="Превышен лимит запросов"):
        super().__init__(message, 429)

class ConfigurationError(BaseAppException):
    """Исключение для ошибок конфигурации"""
    def __init__(self, message):
        super().__init__(message, 500)