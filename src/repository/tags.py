# from sqlalchemy import select, and_
# from sqlalchemy.ext.asyncio import AsyncSession

# from src.entity.models import Tag, User
# from src.schemas.tags import TagSchema


# async def get_tags(skip: int, limit: int, db: AsyncSession, user: User):
#     #stmt = select(Tag).filter_by(user=user).offset(offset).limit(limit) ###когда будут юзеры модели и прочее
#     """
#     The get_tags function returns a list of tags.
    
#     :param skip: int: Skip the first n tags in the database
#     :param limit: int: Limit the number of results returned
#     :param db: AsyncSession: Pass the database connection to the function
#     :param user: User: Filter the results by user
#     :return: A list of tags
#     :doc-author: Trelent
#     """
#     stmt = select(Tag).filter_by(user=user).offset(skip).limit(limit)
#     contacts = await db.execute(stmt)
#     return contacts.scalars().all()


# async def get_tag(tag_id: int, db: AsyncSession, user: User):
#     #stmt = select(Tag).filter_by(id=tag_id, user=user)###когда будут юзеры модели и прочее
#     """
#     The get_tag function returns a single tag from the database.
        
        
    
#     :param tag_id: int: Specify the tag id
#     :param db: AsyncSession: Pass the database connection to the function
#     :param user: User: Specify the user who created the tag
#     :return: A single tag from the database
#     :doc-author: Trelent
#     """
#     stmt = select(Tag).filter_by(id=tag_id, user=user)
#     contact = await db.execute(stmt)
#     return contact.scalar_one_or_none()


# async def create_tag(body: TagSchema, db: AsyncSession, user: User) -> Tag:
#     #tag = Tag(**body.model_dump(exclude_unset=True), user=user)###когда будут юзеры модели и прочее 
#     """
#     The create_tag function creates a new tag in the database.
    
#     :param body: TagSchema: Validate the request body
#     :param db: AsyncSession: Pass the database session to the function
#     :param user: User: Get the user that created the tag
#     :return: A tag object
#     :doc-author: Trelent
#     """
#     tag = Tag(**body.model_dump(exclude_unset=True), user=user) 
#     db.add(tag)
#     await db.commit()
#     await db.refresh(tag)
#     return tag


# async def remove_tag(tag_id: int, db: AsyncSession, user: User)  -> Tag | None:
#     #stmt = select(tag).filter_by(id=tag_id, user=user)###когда будут юзеры модели и прочее
#     """
#     The remove_tag function removes a tag from the database.
        
        
    
#     :param tag_id: int: Get the tag with that id from the database
#     :param db: AsyncSession: Pass the database connection to the function
#     :param user: User: Make sure that a user can only delete their own tags
#     :return: The tag object that was deleted
#     :doc-author: Trelent
#     """
#     stmt = select(Tag).filter_by(id=tag_id, user=user)
#     tag = await db.execute(stmt)
#     tag = tag.scalar_one_or_none()
#     if tag:
#         await db.delete(tag)
#         await db.commit()
#     return tag
