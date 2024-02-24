from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.entity.models import Comment
from src.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from src.entity.models import Role, Image
from typing import List, Optional
from select import select


async def create_comment(
    db: AsyncSession, photo_id: int, comment: CommentCreate, user_id: int
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
    db_comment = Comment(image_id=photo_id, user_id=user_id, content=comment.content)
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment


async def update_comment(
    db: AsyncSession, comment_id: int, user_id: int, content: str
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
    comment = await db.get(Comment, comment_id)
    if comment and comment.user_id == user_id:
        if content.strip():
            comment.content = content
            comment.updated_at = datetime.utcnow()
            await db.commit()
            return comment
    return None


async def delete_comment(
    db: AsyncSession, comment_id: int, user_role: Role
) -> CommentResponse:
    """
    The delete_comment function deletes a comment from the database.

    :param db: AsyncSession: Pass the database connection to the function
    :param comment_id: int: The ID of the comment to be deleted
    :param user_role: UserRole: The role of the user attempting to delete the comment
    :return: The deleted comment object if successful, None otherwise
    :doc-author: YourName
    """
    comment = await db.get(Comment, comment_id)
    if comment:
        if user_role in [Role.admin, Role.moderator]:
            db.delete(comment)
            await db.commit()
            return comment
    return None


async def get_all_comments(db: AsyncSession) -> List[CommentResponse]:
    """
    The get_all_comments function retrieves all comments from the database.

    :param db: AsyncSession: Pass the database connection to the function
    :return: A list of all comments
    :doc-author: YourName
    """
    return await db.execute(select(Comment)).scalars().all()


async def get_comment_by_id(
    db: AsyncSession, comment_id: int
) -> Optional[CommentResponse]:
    """
    The get_comment_by_id function retrieves a comment by its ID from the database.

    :param db: AsyncSession: Pass the database connection to the function
    :param comment_id: int: The ID of the comment to retrieve
    :return: The retrieved comment object if found, None otherwise
    :doc-author: YourName
    """
    return await db.get(Comment, comment_id)
