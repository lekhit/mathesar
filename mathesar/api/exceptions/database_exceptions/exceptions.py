from rest_framework import status

from mathesar.api.exceptions.database_exceptions.base_exceptions import ProgrammingAPIException
from mathesar.api.exceptions.error_codes import ErrorCodes
from mathesar.api.exceptions.generic_exceptions.base_exceptions import (
    MathesarAPIException,
    get_default_exception_detail,
)


class UniqueViolationAPIException(MathesarAPIException):
    error_code = ErrorCodes.UniqueViolation.value

    def __init__(
            self,
            exception,
            message="This column has non-unique values so a unique constraint cannot be set",
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        exception_detail = get_default_exception_detail(exception, self.error_code, message, field, details)._asdict()
        self.detail = [exception_detail]
        self.status_code = status_code


class DuplicateTableAPIException(ProgrammingAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.DuplicateTableError.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class DuplicateColumnAPIException(ProgrammingAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.DuplicateColumnError.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class InvalidDefaultAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.InvalidDefault.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class InvalidTypeOptionAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.InvalidTypeOption.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class InvalidTypeCastAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.InvalidTypeCast.value

    def __init__(
            self,
            exception,
            message="Invalid type cast requested.",
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class DynamicDefaultAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.UndefinedFunction.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class UnsupportedTypeAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.UnsupportedType.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class BadFilterAPIException(MathesarAPIException):
    error_code = ErrorCodes.UnsupportedType.value

    def __init__(
            self,
            exception,
            message="Filter arguments are not correct",
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class BadSortAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.UnsupportedType.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class BadGroupAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.UnsupportedType.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class RaiseExceptionAPIException(MathesarAPIException):
    """
    Exception raised inside a postgres function
    """
    error_code = ErrorCodes.RaiseException.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)


class UndefinedFunctionAPIException(MathesarAPIException):
    # Default message is not needed as the exception string provides enough details
    error_code = ErrorCodes.UndefinedFunction.value

    def __init__(
            self,
            exception,
            message=None,
            field=None,
            details=None,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        super().__init__(exception, self.error_code, message, field, details, status_code)
