from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database.db import get_db
from src.repository import comments as repo_comments
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from src.services import auth_service
from src.entity.models import User, Role
from src.services.roles import RoleAccess
from src.repository import images as repository_images
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession

access_to_delete = RoleAccess([Role.admin, Role.moderator])

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("/", response_model=CommentResponse, status_code=201)
async def create_comment(
    body: CommentCreate,
    image_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The create_comment function creates a new comment.
    
    :param body: CommentCreate: Pass the comment data to the function
    :param image_id: int: Get the image id from the url
    :param db: AsyncSession: Pass the database session to the repository layer
    :param user: User: Get the current user
    :param : Get the image id from the url
    :return: A comment object
    :doc-author: Trelent
    """
    existing_image = await repository_images.get_others_image(image_id, db, user)
    print(f"eto image{existing_image}")
    if not existing_image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with id {image_id} not found",
        )
    created_comment = await repo_comments.create_comment(
        body, db, existing_image.id, user=user
    )
    return created_comment


@router.patch("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    body: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    
    """
    The update_comment function updates a comment in the database.
    
    :param comment_id: int: Identify the comment to be updated
    :param body: CommentCreate: Pass the new comment content to the update_comment function
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user
    :param : Get the comment id from the url
    :return: The updated comment
    :doc-author: Trelent
    """
    updated_comment = await repo_comments.update_comment(
        db, comment_id, current_user.id, body
    )
    if not updated_comment:
        raise HTTPException(
            status_code=400, detail="Cannot update comment with empty content"
        )
    # elif (
    #     not updated_comment.comment.strip()
    # ):  # Перевірка, чи не є вміст коментаря пустим після редагування
    #     # Якщо вміст коментаря порожній після редагування, вважаємо це спробою видалення коментаря
    #     raise HTTPException(
    #         status_code=400, detail="Cannot update comment with empty content"
    #     )
    return updated_comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):

    """
    The delete_comment function deletes a comment from the database.
        The function takes in an integer representing the id of the comment to be deleted,
        and returns a dictionary containing information about whether or not 
        deletion was successful.
    
    :param comment_id: int: Specify the comment id of the comment to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :param current_user: User: Get the current user and check if they are an admin or not
    :param : Get the comment id from the url
    :return: A comment object
    :doc-author: Trelent
    """
    deleted_comment = await repo_comments.delete_comment(
        db, comment_id, current_user.role
    )
    return deleted_comment
