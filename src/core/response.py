from typing import Any, Optional, Dict, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    data: T
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    success: bool = False
    statusCode: int
    errorMessage: str
    details: Optional[Dict[str, Any]] = None


# Specific response models for different endpoints
class NoteResponse(BaseModel):
    id: str
    title: str
    content: str
    owner_uid: str
    is_favorite: bool
    tags: list[str]
    sync_status: str
    last_synced_at: str
    created_at: str
    updated_at: str


class NotesListResponse(BaseModel):
    success: bool = True
    data: list[NoteResponse]
    message: Optional[str] = None


class NoteCreateResponse(BaseModel):
    success: bool = True
    data: NoteResponse
    message: Optional[str] = None


class NoteUpdateResponse(BaseModel):
    success: bool = True
    data: NoteResponse
    message: Optional[str] = None


class NoteDeleteResponse(BaseModel):
    success: bool = True
    data: Optional[None] = None
    message: Optional[str] = None


# Tag response models
class TagResponse(BaseModel):
    id: str
    name: str
    created_at: str


class TagsListResponse(BaseModel):
    success: bool = True
    data: list[TagResponse]
    message: Optional[str] = None


class TagCreateResponse(BaseModel):
    success: bool = True
    data: TagResponse
    message: Optional[str] = None


class TagUpdateResponse(BaseModel):
    success: bool = True
    data: TagResponse
    message: Optional[str] = None


class TagDeleteResponse(BaseModel):
    success: bool = True
    data: Optional[None] = None
    message: Optional[str] = None
