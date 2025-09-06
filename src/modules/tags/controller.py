from fastapi import APIRouter, Depends, status
from src.modules.tags.models import TagCreate, TagUpdate
from src.modules.auth.service import AuthService
from src.core.response import (
    TagCreateResponse,
    TagsListResponse,
    TagUpdateResponse,
    TagDeleteResponse
)
from src.modules.tags.service import TagService

router = APIRouter(
    prefix="/api/tags",
    tags=["Tags"]
)

# Create a new tag
@router.post("/", response_model=TagCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(tag: TagCreate, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Create a new tag."""
    tag_response = await TagService.create_tag(tag, current_uid)
    return TagCreateResponse(
        data=tag_response,
        message="Tag created successfully"
    )

# Get all tags for the logged in user
@router.get("/", response_model=TagsListResponse)
async def get_user_tags(current_uid: str = Depends(AuthService.get_current_user_uid)):
    """List all tags for the logged in user."""
    tags = await TagService.get_user_tags(current_uid)
    return TagsListResponse(
        data=tags,
        message=f"Retrieved {len(tags)} tags"
    )

# Update a tag
@router.put("/{tag_id}", response_model=TagUpdateResponse)
async def update_tag(tag_id: str, tag_update: TagUpdate, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Update the tag with the specified ID. Only the tag owner can update it."""
    updated_tag = await TagService.update_tag(tag_id, tag_update, current_uid)
    return TagUpdateResponse(
        data=updated_tag,
        message="Tag updated successfully"
    )

# Delete a tag
@router.delete("/{tag_id}", response_model=TagDeleteResponse)
async def delete_tag(tag_id: str, current_uid: str = Depends(AuthService.get_current_user_uid)):
    """Delete the tag with the specified ID. Only the tag owner can delete it."""
    await TagService.delete_tag(tag_id, current_uid)
    return TagDeleteResponse(
        data=None,
        message="Tag deleted successfully"
    )
