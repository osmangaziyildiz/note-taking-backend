from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from src.core.logging import configure_logging, LogLevels
from src.core.config import settings
from src.core.routes import register_routes, register_exception_handlers

# Configure logging
configure_logging(settings.LOG_LEVEL)

app = FastAPI(title="Notes API", version="1.0.0")

# CORS (Cross-Origin Resource Sharing) Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all routes and exception handlers
register_routes(app)
register_exception_handlers(app)

@app.get("/", include_in_schema=False)
async def read_root():
    return {"message": "Welcome to the Notes API. \n This API Made by Osmangazi YILDIZ"}

@app.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": "Notes API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }