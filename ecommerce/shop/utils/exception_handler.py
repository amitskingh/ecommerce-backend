from rest_framework.views import exception_handler
from rest_framework import status
from .response_wrapper import error_response
import traceback


def custom_exception_handler(exc, context):
    """
    Custom exception handler that ensures all API errors return
    a consistent JSON structure using `error_response`.
    """

    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Handle known DRF exceptions (ValidationError, NotFound, etc.)
        message = (
            response.data.get("detail") if isinstance(response.data, dict) else None
        )

        # If 'detail' is missing (e.g., serializer validation error)
        if not message:
            message = (
                "Validation error"
                if response.status_code == 400
                else "Something went wrong"
            )

        return error_response(
            message=message,
            errors=response.data,
            status_code=response.status_code,
        )

    # Handle unexpected/unhandled exceptions (like 500s)
    else:
        # Log full stack trace for debugging (optional)
        print("UNHANDLED EXCEPTION:", str(exc))
        traceback.print_exc()

        return error_response(
            message="Internal server error",
            errors={"detail": str(exc)},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
