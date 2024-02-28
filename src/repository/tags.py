from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Tag, User, Image
from src.schemas.tags import TagSchema


# bind images and tags
async def get_tag(tag_id: int, db: AsyncSession, user: User):
    """
    The get_tag function returns a single tag from the database.
    
    :param tag_id: int: Specify the tag id
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Specify the user who created the tag
    :return: A single tag from the database
    :doc-author: Trelent
    """
    stmt = select(Tag).filter_by(id=tag_id, user=user)
    tag = await db.execute(stmt)
    return tag.unique().scalar_one_or_none()


async def get_tag_by_name(db: AsyncSession, name):
    """
    The get_tag_by_name function returns a tag object from the database.
    
    :param db: AsyncSession: Pass the database session to the function
    :param name: Filter the tag by name
    :return: A tag object from the database
    :doc-author: Trelent
    """
    stmt = select(Tag).filter_by(name=name)
    tag = await db.execute(stmt)
    return tag.unique().scalar_one_or_none()


# dont delete, we use it for images
async def create_tag(body: str, db: AsyncSession, user: User) -> Tag:
    """
    The create_tag function creates a new tag in the database.
    
    :param body: str: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user that created the tag
    :return: A tag object
    :doc-author: Trelent
    """
    existed_tag = await get_tag_by_name(db, body)
    print(existed_tag)
    if existed_tag:
        return existed_tag
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     detail="Tag with this name already exists",
        # )
    else:
        tag = Tag(name=body, user=user)

    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def remove_tag(tag_id: int, db: AsyncSession, user: User) -> None:
    """
    The remove_tag function removes a tag from the database.
    
    :param tag_id: int: Get the tag with that id from the database
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Make sure that a user can only delete their own tags
    :return: The tag object that was deleted
    :doc-author: Trelent
    """
    stmt = select(Tag).filter_by(id=tag_id, user=user)
    tag = await db.execute(stmt)
    tag = tag.unique().scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()
    return tag
