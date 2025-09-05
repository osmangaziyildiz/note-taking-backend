from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from typing import Optional, Any, Dict
from pydantic import BaseModel, ValidationError


# ============================================================================
# ERROR MODELS
# ============================================================================

class ErrorResponse(BaseModel):
    success: bool = False
    statusCode: int
    errorMessage: str
    details: Optional[Dict[str, Any]] = None


# ============================================================================
# CUSTOM EXCEPTIONS
# ============================================================================

class CustomHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_message = error_message
        self.details = details
        
        super().__init__(
            status_code=status_code,
            detail={
                "success": False,
                "statusCode": status_code,
                "errorMessage": error_message,
                "details": details
            }
        )


class NotFoundError(CustomHTTPException):
    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message += f" with ID: {resource_id}"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_message=message
        )


class UnauthorizedError(CustomHTTPException):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_message=message
        )


class ForbiddenError(CustomHTTPException):
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_message=message
        )


class ValidationError(CustomHTTPException):
    def __init__(self, message: str = "Validation failed", details: Dict[str, Any] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_message=message,
            details=details
        )


class InternalServerError(CustomHTTPException):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_message=message
        )


# ============================================================================
# EXCEPTION HANDLERS
# ============================================================================

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors and convert to our standard format."""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "statusCode": 422,
            "errorMessage": "Validation failed",
            "details": {
                "validation_errors": errors
            }
        }
    )


async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    """Handle our custom HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "statusCode": exc.status_code,
            "errorMessage": exc.error_message,
            "details": exc.details
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI's default HTTP exceptions (like from HTTPBearer)."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "statusCode": exc.status_code,
            "errorMessage": exc.detail,
            "details": None
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "statusCode": 500,
            "errorMessage": "Internal server error",
            "details": None
        }
    )
