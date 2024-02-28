from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.services.auth import auth_service
from src.database.db import get_db
from src.entity.models import User
from src.schemas.tags import TagSchema, TagResponse
from src.repository import tags as repository_tags

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/{tag_id}", response_model=TagResponse)
async def read_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The read_tag function returns a single tag from the database.
        The function takes in an integer as its argument, which is the ID of the tag to be returned.
        If no such tag exists, then a 404 error is raised.
    
    :param tag_id: int: Specify the id of the tag to be updated
    :param db: Session: Pass the database session to the function
    :param user: User: Pass the current user to the function
    :param : Specify the id of the tag to be updated
    :return: A single tag from the database
    :doc-author: Trelent
    """
    tag = await repository_tags.get_tag(tag_id, db, user)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag

'''
@router.post("/", response_model=TagResponse)
async def create_tag(
    body: TagSchema,
    db: Session = Depends(get_db),
    limit: int = 5,
    user: User = Depends(auth_service.get_current_user),
):
    """
    The create_tag function creates a new tag in the database.
            The function takes a TagSchema object as input and returns the created tag.



    :param body: TagSchema: Validate the data that is passed into the function
    :param db: Session: Pass the database session to the repository layer
    :param user: User: Get the user object from the auth_service
    :return: A tag object, which is a pydantic model
    :doc-author: Trelent
    """
    existing_tag = await repository_tags.get_tag_by_name(db, body.name)
    if existing_tag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists",
        )

    return await repository_tags.create_tag(body, db, user, limit)
'''

@router.delete("/{tag_id}")
async def remove_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The remove_tag function removes a tag from the database.
        Args:
            tag_id (int): The id of the tag to be removed.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
    
    :param tag_id: int: Specify the id of the tag to be retrieved
    :param db: Session: Pass the database session to the repository function
    :param user: User: Get the current user from the database
    :param : Specify the id of the tag to be retrieved
    :return: A tag object
    :doc-author: Trelent
    """
    tag = await repository_tags.remove_tag(tag_id, db, user)
    if tag is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found"
        )
    return tag
