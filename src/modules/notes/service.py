from datetime import datetime
from typing import List
from src.core.firebase import db
from src.modules.notes.models import NoteCreate, NoteUpdate, NoteInDB
from src.core.response import NoteResponse
from src.core.error_handling import NotFoundError, ForbiddenError, ValidationError, InternalServerError
import logging

NOTES_COLLECTION = "notes"
USER_NOTES_SUBCOLLECTION = "userNotes"

class NoteService:
    @staticmethod
    async def create_note(note: NoteCreate, current_uid: str) -> NoteResponse:
        """Create a new note."""
        try:
            now = datetime.utcnow()
            note_data = note.dict()
            note_data.update({
                "owner_uid": current_uid,
                "tags": [],  # Automatically add empty tags list
                "created_at": now,
                "updated_at": now
            })

            # Create note in nested collection: notes/{userId}/userNotes/{noteId}
            user_notes_ref = db.collection(NOTES_COLLECTION).document(current_uid).collection(USER_NOTES_SUBCOLLECTION)
            update_time, doc_ref = user_notes_ref.add(note_data)
            created_note = doc_ref.get().to_dict()
            
            note_response = NoteResponse(
                id=doc_ref.id,
                title=created_note["title"],
                content=created_note["content"],
                owner_uid=created_note["owner_uid"],
                is_favorite=created_note["is_favorite"],
                tags=created_note["tags"],
                created_at=created_note["created_at"].isoformat(),
                updated_at=created_note["updated_at"].isoformat()
            )
            
            logging.info(f"Created new note {doc_ref.id} for user: {current_uid}")
            return note_response
        except Exception as e:
            logging.error(f"Failed to create note for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to create note. Please try again.")

    @staticmethod
    async def get_user_notes(current_uid: str) -> List[NoteResponse]:
        """Get all notes for the logged in user."""
        try:
            notes = []
            # Query nested collection: notes/{userId}/userNotes
            user_notes_ref = db.collection(NOTES_COLLECTION).document(current_uid).collection(USER_NOTES_SUBCOLLECTION)
            docs = user_notes_ref.stream()
            
            for doc in docs:
                note_data = doc.to_dict()
                note_response = NoteResponse(
                    id=doc.id,
                    title=note_data["title"],
                    content=note_data["content"],
                    owner_uid=note_data["owner_uid"],
                    is_favorite=note_data["is_favorite"],
                    tags=note_data["tags"],
                    created_at=note_data["created_at"].isoformat(),
                    updated_at=note_data["updated_at"].isoformat()
                )
                notes.append(note_response)
            
            logging.info(f"Retrieved {len(notes)} notes for user: {current_uid}")
            return notes
        except Exception as e:
            logging.error(f"Failed to retrieve notes for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to retrieve notes. Please try again.")

    @staticmethod
    async def update_note(note_id: str, note_update: NoteUpdate, current_uid: str) -> NoteResponse:
        """Update the note with the specified ID."""
        try:
            # Access nested collection: notes/{userId}/userNotes/{noteId}
            doc_ref = db.collection(NOTES_COLLECTION).document(current_uid).collection(USER_NOTES_SUBCOLLECTION).document(note_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                logging.warning(f"Note {note_id} not found for user {current_uid}")
                raise NotFoundError("Note", note_id)
            
            # No need to check owner_uid since we're already in the user's collection
            update_data = note_update.dict(exclude_unset=True)
            if not update_data:
                raise ValidationError("No fields to update")

            # Only update updated_at if content-related fields are being updated
            if "title" in update_data or "content" in update_data:
                update_data["updated_at"] = datetime.utcnow()
            
            doc_ref.update(update_data)
            
            updated_doc = doc_ref.get()
            updated_note_data = updated_doc.to_dict()
            updated_note = NoteResponse(
                id=updated_doc.id,
                title=updated_note_data["title"],
                content=updated_note_data["content"],
                owner_uid=updated_note_data["owner_uid"],
                is_favorite=updated_note_data["is_favorite"],
                tags=updated_note_data["tags"],
                created_at=updated_note_data["created_at"].isoformat(),
                updated_at=updated_note_data["updated_at"].isoformat()
            )
            
            logging.info(f"Updated note {note_id} for user: {current_uid}")
            return updated_note
        except (NotFoundError, ForbiddenError, ValidationError):
            raise
        except Exception as e:
            logging.error(f"Failed to update note {note_id} for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to update note. Please try again.")

    @staticmethod
    async def delete_note(note_id: str, current_uid: str) -> None:
        """Delete the note with the specified ID."""
        try:
            # Access nested collection: notes/{userId}/userNotes/{noteId}
            doc_ref = db.collection(NOTES_COLLECTION).document(current_uid).collection(USER_NOTES_SUBCOLLECTION).document(note_id)
            doc = doc_ref.get()

            if not doc.exists:
                logging.warning(f"Note {note_id} not found for user {current_uid}")
                raise NotFoundError("Note", note_id)

            # No need to check owner_uid since we're already in the user's collection
            doc_ref.delete()
            logging.info(f"Deleted note {note_id} for user: {current_uid}")
        except (NotFoundError, ForbiddenError):
            raise
        except Exception as e:
            logging.error(f"Failed to delete note {note_id} for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to delete note. Please try again.")

    @staticmethod
    async def toggle_favorite(note_id: str, current_uid: str) -> NoteResponse:
        """Toggle favorite status of a note."""
        try:
            # Access nested collection: notes/{userId}/userNotes/{noteId}
            doc_ref = db.collection(NOTES_COLLECTION).document(current_uid).collection(USER_NOTES_SUBCOLLECTION).document(note_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                logging.warning(f"Note {note_id} not found for user {current_uid}")
                raise NotFoundError("Note", note_id)
            
            # Toggle the favorite status
            current_favorite = doc.to_dict()["is_favorite"]
            new_favorite = not current_favorite
            
            doc_ref.update({
                "is_favorite": new_favorite
            })
            
            # Get updated note data
            updated_doc = doc_ref.get()
            updated_note_data = updated_doc.to_dict()
            updated_note = NoteResponse(
                id=updated_doc.id,
                title=updated_note_data["title"],
                content=updated_note_data["content"],
                owner_uid=updated_note_data["owner_uid"],
                is_favorite=updated_note_data["is_favorite"],
                tags=updated_note_data["tags"],
                created_at=updated_note_data["created_at"].isoformat(),
                updated_at=updated_note_data["updated_at"].isoformat()
            )
            
            action = "added to" if new_favorite else "removed from"
            logging.info(f"Note {note_id} {action} favorites for user: {current_uid}")
            return updated_note
        except (NotFoundError, ForbiddenError):
            raise
        except Exception as e:
            logging.error(f"Failed to toggle favorite for note {note_id} and user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to toggle favorite. Please try again.")
