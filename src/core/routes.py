from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from src.modules.notes.controller import router as notes_router
from src.modules.auth.controller import router as auth_router
from src.core.error_handling import (
    CustomHTTPException,
    validation_exception_handler,
    custom_http_exception_handler,
    http_exception_handler,
    general_exception_handler
)


def register_routes(app: FastAPI) -> None:
    """
    Register all application routes.
    
    Args:
        app: FastAPI application instance
    """

    # Authentication routes
    app.include_router(auth_router)

    # Notes routes
    app.include_router(notes_router)
    


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all application exception handlers.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(CustomHTTPException, custom_http_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
