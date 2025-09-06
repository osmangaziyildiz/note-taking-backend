from fastapi import APIRouter, Depends, status
from src.modules.notes.models import NoteCreate, NoteUpdate
from src.modules.auth.service import AuthService
from src.core.response import (
    NoteCreateResponse,
    NotesListResponse,
    NoteUpdateResponse,
    NoteDeleteResponse
)
from src.modules.notes.service import NoteService

router = APIRouter(
    prefix="/api/notes",
    tags=["Notes"]
)

# Create a new note
@router.post("/", response_model=NoteCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_note(note: NoteCreate, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Create a new note."""
    note_response = await NoteService.create_note(note, current_uid)
    return NoteCreateResponse(
        data=note_response,
        message="Note created successfully"
    )

# Get all notes for the logged in user
@router.get("/", response_model=NotesListResponse)
async def get_user_notes(current_uid: str = Depends(AuthService.get_current_user_uid)):
    """List all notes for the logged in user."""
    notes = await NoteService.get_user_notes(current_uid)
    return NotesListResponse(
        data=notes,
        message=f"Retrieved {len(notes)} notes"
    )

# Get a specific note by ID
@router.get("/{note_id}", response_model=NoteUpdateResponse)
async def get_note_by_id(note_id: str, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Get a specific note by ID. Only the note owner can access it."""
    note = await NoteService.get_note_by_id(note_id, current_uid)
    return NoteUpdateResponse(
        data=note,
        message="Note retrieved successfully"
    )

# Update a note
@router.put("/{note_id}", response_model=NoteUpdateResponse)
async def update_note(note_id: str, note_update: NoteUpdate, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Update the note with the specified ID. Only the note owner can update it."""
    updated_note = await NoteService.update_note(note_id, note_update, current_uid)
    return NoteUpdateResponse(
        data=updated_note,
        message="Note updated successfully"
    )

# Delete a note
@router.delete("/{note_id}", response_model=NoteDeleteResponse)
async def delete_note(note_id: str, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Delete the note with the specified ID. Only the note owner can delete it."""
    await NoteService.delete_note(note_id, current_uid)
    return NoteDeleteResponse(
        data=None,
        message="Note deleted successfully"
    )

# Toggle favorite status of a note
@router.patch("/{note_id}/favorite", response_model=NoteUpdateResponse)
async def toggle_favorite(note_id: str, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Toggle favorite status of a note. Only the note owner can toggle it."""
    updated_note = await NoteService.toggle_favorite(note_id, current_uid)
    favorite_status = "added to" if updated_note.is_favorite else "removed from"
    return NoteUpdateResponse(
        data=updated_note,
        message=f"Note {favorite_status} favorites successfully"
    )
