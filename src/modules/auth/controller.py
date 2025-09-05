from fastapi import APIRouter, Depends
from src.modules.auth.service import AuthService
from src.modules.auth.models import TokenData

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# Authentication endpoints
@router.get("/me")
async def get_current_user(current_user: TokenData = Depends(AuthService.get_current_user_data)):
    """Get current user information."""
    return {
        "success": True,
        "data": current_user.dict(),
        "message": "User information retrieved successfully"
    }

@router.get("/verify")
async def verify_token(current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Verify if token is valid."""
    return {
        "success": True,
        "data": {"uid": current_uid},
        "message": "Token is valid"
    }
