from datetime import datetime
from typing import List
from src.core.firebase import db
from src.modules.notes.models import NoteCreate, NoteUpdate, NoteInDB
from src.core.response import NoteResponse
from src.core.error_handling import NotFoundError, ForbiddenError, ValidationError, InternalServerError
import logging

NOTES_COLLECTION = "notes"

class NoteService:
    @staticmethod
    async def create_note(note: NoteCreate, current_uid: str) -> NoteResponse:
        """Create a new note."""
        try:
            now = datetime.utcnow()
            note_data = note.dict()
            note_data.update({
                "owner_uid": current_uid,
                "created_at": now,
                "updated_at": now
            })

            update_time, doc_ref = db.collection(NOTES_COLLECTION).add(note_data)
            created_note = doc_ref.get().to_dict()
            
            note_response = NoteResponse(
                id=doc_ref.id,
                title=created_note["title"],
                content=created_note["content"],
                owner_uid=created_note["owner_uid"],
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
            docs = db.collection(NOTES_COLLECTION).where("owner_uid", "==", current_uid).stream()
            for doc in docs:
                note_data = doc.to_dict()
                note_response = NoteResponse(
                    id=doc.id,
                    title=note_data["title"],
                    content=note_data["content"],
                    owner_uid=note_data["owner_uid"],
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
            doc_ref = db.collection(NOTES_COLLECTION).document(note_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                logging.warning(f"Note {note_id} not found for user {current_uid}")
                raise NotFoundError("Note", note_id)
            
            note_data = doc.to_dict()
            if note_data["owner_uid"] != current_uid:
                logging.warning(f"User {current_uid} not authorized to update note {note_id}")
                raise ForbiddenError("You are not authorized to update this note")
                
            update_data = note_update.dict(exclude_unset=True)
            if not update_data:
                raise ValidationError("No fields to update")

            update_data["updated_at"] = datetime.utcnow()
            doc_ref.update(update_data)
            
            updated_doc = doc_ref.get()
            updated_note = NoteResponse(
                id=updated_doc.id,
                title=updated_doc.to_dict()["title"],
                content=updated_doc.to_dict()["content"],
                owner_uid=updated_doc.to_dict()["owner_uid"],
                created_at=updated_doc.to_dict()["created_at"].isoformat(),
                updated_at=updated_doc.to_dict()["updated_at"].isoformat()
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
            doc_ref = db.collection(NOTES_COLLECTION).document(note_id)
            doc = doc_ref.get()

            if not doc.exists:
                logging.warning(f"Note {note_id} not found for user {current_uid}")
                raise NotFoundError("Note", note_id)

            if doc.to_dict()["owner_uid"] != current_uid:
                logging.warning(f"User {current_uid} not authorized to delete note {note_id}")
                raise ForbiddenError("You are not authorized to delete this note")
                
            doc_ref.delete()
            logging.info(f"Deleted note {note_id} for user: {current_uid}")
        except (NotFoundError, ForbiddenError):
            raise
        except Exception as e:
            logging.error(f"Failed to delete note {note_id} for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to delete note. Please try again.")
