from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.entity.models import Comment, User
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from src.entity.models import Role, Image
from typing import List, Optional
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from src.repository.images import is_object_added


async def create_comment(
    body: CommentCreate, db: AsyncSession, existing_image: int, user: User
) -> CommentResponse:
    """
    The create_comment function creates a new comment in the database.

    :param db: AsyncSession: Pass the database connection to the function
    :param photo_id: int: The ID of the photo for which the comment is being created
    :param comment: CommentCreate: The comment data
    :param user_id: int: The ID of the user creating the comment
    :return: The created comment object
    :doc-author: YourName
    """
    comment = Comment(
        **body.model_dump(exclude_unset=True), user=user, image_id=existing_image
    )
    #if not is_object_added(db, comment):
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    return comment


async def update_comment(
    db: AsyncSession, comment_id: int, user_id: int, content: CommentCreate
) -> CommentResponse:
    """
    The update_comment function updates an existing comment in the database.

    :param db: AsyncSession: Pass the database connection to the function
    :param comment_id: int: The ID of the comment to be updated
    :param user_id: int: The ID of the user who created the comment
    :param content: str: The new content of the comment
    :return: The updated comment object if successful, None otherwise
    :doc-author: YourName
    """
    query = select(Comment).filter_by(id=comment_id, user_id=user_id)
    responce = await db.execute(query)
    comment = responce.unique().scalar_one_or_none()
    if not comment.comment.strip():
        comment.comment = content.comment
        comment.updated_at = datetime.utcnow()
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    return None


async def delete_comment(db: AsyncSession, comment_id: int, user_role: Role) -> None:
    """
    The delete_comment function deletes a comment from the database.

    :param db: AsyncSession: Pass the database connection to the function
    :param comment_id: int: The ID of the comment to be deleted
    :param user_role: UserRole: The role of the user attempting to delete the comment
    :return: The deleted comment object if successful, None otherwise
    :doc-author: YourName
    """
    query = select(Comment).filter_by(id=comment_id)
    responce = await db.execute(query)
    comment = responce.unique().scalar_one_or_none()
    if comment:
        if user_role in [Role.admin, Role.moderator]:
            await db.delete(comment)
            await db.commit()
            return comment
        raise HTTPException(
            status_code=403,
            detail="Forbidden: You don't have permission to delete comments",
        )
    raise HTTPException(status_code=404, detail="Comment not found")
