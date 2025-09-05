from pydantic import BaseModel
from typing import Optional

class UserInfo(BaseModel):
    """User information from Firebase token."""
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None

class TokenData(BaseModel):
    """Token data for authentication."""
    uid: str
    email: Optional[str] = None
    name: Optional[str] = None
