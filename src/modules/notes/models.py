from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    is_favorite: bool = Field(default=False, description="Whether the note is marked as favorite")


class NoteCreate(NoteBase):
    id: str = Field(..., min_length=1, description="Note ID provided by client")


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = None
    is_favorite: Optional[bool] = Field(None, description="Whether the note is marked as favorite")


class NoteInDB(NoteBase):
    id: str
    owner_uid: str
    tags: list[str] = Field(default_factory=list, description="List of tags for the note")
    created_at: datetime
    updated_at: datetime
