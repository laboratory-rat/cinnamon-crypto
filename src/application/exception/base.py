from typing import Type


class AppException(Exception):
    service_type: Type
    code: str
    inner_exception: Exception = None

    def __init__(self, service_type: Type, code: str, message: object, inner_exception: Exception = None):
        super().__init__(message)
        self.service_type = service_type
        self.code = code
        self.inner_exception = inner_exception


class AppNotFoundException(AppException):
    def __init__(self, service_type: Type, entity_type: Type, key: object, value: object, inner_exception: Exception = None):
        super().__init__(service_type, 'NOT_FOUND', f"Object of type {entity_type.__name__} was not found by {key}:{value}", inner_exception)
