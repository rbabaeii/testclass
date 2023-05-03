from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework.views import exception_handler


class SomethingWrongHappened(exceptions.APIException):
    status_code = 500
    default_code = "something_happened"


class ValidationError(exceptions.APIException):
    status_code = 400
    default_code = "invalid_inputs"


class NotAllowedError(exceptions.APIException):
    status_code = 401
    default_code = "permission_denied"


class ErrorHandler:
    default_message = _("Something wrong happened, we are working on it!")
    default_exception = SomethingWrongHappened

    messages = {
        400: {
            'general': _('Provided form fields have some problems or not filled'),
            'reply_error': _('bad request for reply'),
            'invalid_image': 'عکس معتبر نیست',
            'invalid_file': 'فایل معتبر نیست',
            'invalid_discount_code': 'کد تخفیف معتبر نیست',
            'total_price_error': 'مبلغ فاکتور کم تر از کف قیمتی کد تخفیف است',
            'not_enough_balance': 'موجودی کافی نیست'
        },

        401: {
            'general': _("You are not allowed to do this."),
        },

        404: {
            'general': _('Not found'),
        },
        500: {
            "general": _("something wrong with server")
        }
    }

    exception = {
        400: ValidationError,
        401: NotAllowedError,
        404: exceptions.NotFound,
        500: SomethingWrongHappened
    }

    @staticmethod
    def get_error_message(error_code: int, message_id: str):
        """
        Returns a translated message based on the error code and message id
        """
        try:
            message = ErrorHandler.messages[error_code][message_id]
            return message
        except KeyError:
            return ErrorHandler.default_message

    @staticmethod
    def get_error_exception(error_code: int, message_id: str, exception=None) -> Exception:
        """
        Returns an exception based on error code and message id
        """
        try:
            message = ErrorHandler.messages[error_code][message_id]

        except KeyError:
            message = ErrorHandler.default_message

        if exception is None:
            try:
                exception = ErrorHandler.exception[error_code]

            except KeyError:
                exception = ErrorHandler.default_exception

        return exception({"messages": [{"message": message}], "code": message_id})

    @staticmethod
    def create_error_exception(error_code: int, message: str, exception=None) -> Exception:
        """
        Create an exception based on error code and message
        """

        if exception is None:
            try:
                exception = ErrorHandler.exception[error_code]

            except KeyError:
                exception = ErrorHandler.default_exception

        return exception({"messages": [{"message": message}], "code": 4})


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,s
    # to get the standard error response.
    response = exception_handler(exc, context)
    messages = []

    if response and not response.data.get("messages"):
        for message in response.data:
            error_message = response.data[message]
            messages.append(
                {
                    "field": message,
                    "message": error_message if isinstance(error_message, exceptions.ErrorDetail) else error_message[0]
                }
            )
        response.data = {"messages": messages, "code": "serializer_errors"}

    return response
