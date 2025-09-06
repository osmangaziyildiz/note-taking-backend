from datetime import datetime
from typing import List
from src.core.firebase import db
from src.modules.tags.models import TagCreate, TagUpdate, TagInDB
from src.core.response import TagResponse
from src.core.error_handling import NotFoundError, ForbiddenError, ValidationError, InternalServerError
import logging

USER_TAGS_COLLECTION = "userTags"
TAGS_SUBCOLLECTION = "tags"

class TagService:
    @staticmethod
    async def create_tag(tag: TagCreate, current_uid: str) -> TagResponse:
        """Create a new tag."""
        try:
            now = datetime.utcnow()
            tag_data = tag.dict()
            tag_data.update({
                "created_at": now
            })

            # Create tag in nested collection: userTags/{userId}/tags/{tagId}
            user_tags_ref = db.collection(USER_TAGS_COLLECTION).document(current_uid).collection(TAGS_SUBCOLLECTION)
            update_time, doc_ref = user_tags_ref.add(tag_data)
            created_tag = doc_ref.get().to_dict()
            
            tag_response = TagResponse(
                id=doc_ref.id,
                name=created_tag["name"],
                created_at=created_tag["created_at"].isoformat()
            )
            
            logging.info(f"Created new tag {doc_ref.id} for user: {current_uid}")
            return tag_response
        except Exception as e:
            logging.error(f"Failed to create tag for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to create tag. Please try again.")

    @staticmethod
    async def get_user_tags(current_uid: str) -> List[TagResponse]:
        """Get all tags for the logged in user."""
        try:
            tags = []
            # Query nested collection: userTags/{userId}/tags
            user_tags_ref = db.collection(USER_TAGS_COLLECTION).document(current_uid).collection(TAGS_SUBCOLLECTION)
            docs = user_tags_ref.stream()
            
            for doc in docs:
                tag_data = doc.to_dict()
                tag_response = TagResponse(
                    id=doc.id,
                    name=tag_data["name"],
                    created_at=tag_data["created_at"].isoformat()
                )
                tags.append(tag_response)
            
            logging.info(f"Retrieved {len(tags)} tags for user: {current_uid}")
            return tags
        except Exception as e:
            logging.error(f"Failed to retrieve tags for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to retrieve tags. Please try again.")

    @staticmethod
    async def update_tag(tag_id: str, tag_update: TagUpdate, current_uid: str) -> TagResponse:
        """Update the tag with the specified ID."""
        try:
            # Access nested collection: userTags/{userId}/tags/{tagId}
            doc_ref = db.collection(USER_TAGS_COLLECTION).document(current_uid).collection(TAGS_SUBCOLLECTION).document(tag_id)
            doc = doc_ref.get()
            
            if not doc.exists:
                logging.warning(f"Tag {tag_id} not found for user {current_uid}")
                raise NotFoundError("Tag", tag_id)
            
            # No need to check owner_uid since we're already in the user's collection
            update_data = tag_update.dict(exclude_unset=True)
            if not update_data:
                raise ValidationError("No fields to update")

            doc_ref.update(update_data)
            
            updated_doc = doc_ref.get()
            updated_tag_data = updated_doc.to_dict()
            updated_tag = TagResponse(
                id=updated_doc.id,
                name=updated_tag_data["name"],
                created_at=updated_tag_data["created_at"].isoformat()
            )
            
            logging.info(f"Updated tag {tag_id} for user: {current_uid}")
            return updated_tag
        except (NotFoundError, ForbiddenError, ValidationError):
            raise
        except Exception as e:
            logging.error(f"Failed to update tag {tag_id} for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to update tag. Please try again.")

    @staticmethod
    async def delete_tag(tag_id: str, current_uid: str) -> None:
        """Delete the tag with the specified ID."""
        try:
            # Access nested collection: userTags/{userId}/tags/{tagId}
            doc_ref = db.collection(USER_TAGS_COLLECTION).document(current_uid).collection(TAGS_SUBCOLLECTION).document(tag_id)
            doc = doc_ref.get()

            if not doc.exists:
                logging.warning(f"Tag {tag_id} not found for user {current_uid}")
                raise NotFoundError("Tag", tag_id)

            # No need to check owner_uid since we're already in the user's collection
            doc_ref.delete()
            logging.info(f"Deleted tag {tag_id} for user: {current_uid}")
        except (NotFoundError, ForbiddenError):
            raise
        except Exception as e:
            logging.error(f"Failed to delete tag {tag_id} for user {current_uid}. Error: {str(e)}")
            raise InternalServerError("Failed to delete tag. Please try again.")
