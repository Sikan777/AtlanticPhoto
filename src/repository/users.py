from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.database.db import get_db
from src.entity.models import User, Image
from src.schemas.users import UserSchema
from libgravatar import Gravatar
from sqlalchemy import func


# Using the function get user by his/her email
async def get_user_by_email(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_by_email function takes an email address and returns the user object associated with that email.
    If no such user exists, it returns None.
    
    :param email: str: Pass the email of the user to be retrieved
    :param db: AsyncSession: Pass the database session to the function
    :return: The user object associated with the email address passed to it
    :doc-author: Trelent
    """
    statement = select(User).filter_by(email=email)
    user = await db.execute(statement)
    user = user.unique().scalar_one_or_none()
    return user


# Create the user in DB
async def create_user(body: UserSchema, db: AsyncSession = Depends(get_db)):
    """
    The create_user function creates a new user in the database.
    
    :param body: UserSchema: Validate the incoming request body
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    :doc-author: Trelent
    """
    async with db as session:
        user_count = await session.execute(func.count(User.id))
        count = user_count.scalar()
        if count == 0:
            # Database is empty, create the first user as an administrator
            new_user = User(**body.model_dump(), role="admin")
        else:
            avatar = None
            try:
                g = Gravatar(body.email)
                avatar = g.get_image()
            except Exception as err:
                print(err)
            new_user = User(**body.model_dump(), avatar=avatar)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


# Update the refresh token
async def update_token(user: User, token: str | None, db: AsyncSession):
    """
    The update_token function updates the refresh token for a user.
    
    :param user: User: Specify the user object that will be updated
    :param token: str | None: Update the user's refresh token
    :param db: AsyncSession: Pass the database session to the function
    :return: The user object
    :doc-author: Trelent
    """
    user.refresh_token = token
    await db.commit()


# Comfirm the email of the user
async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    The confirmed_email function takes an email address and a database connection,
    and marks the user with that email as confirmed.  It does not return anything.
    
    :param email: str: Specify the email of the user to be confirmed
    :param db: AsyncSession: Pass the database connection to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True  # нет такой колонки в моделях юзеров
    await db.commit()


async def delete_access_token(email: str, db: AsyncSession) -> None:
    """
    The delete_access_token function is used to delete the access token of a user.
    This function is called when a user logs out, or if an admin wants to logout another user.
    
    :param email: str: Specify the email of the user
    :param db: AsyncSession: Pass the database connection to the function
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.access_token = None  # то же самое, где такой атрибут в юзерах? Оно ругается
    user.status = False
    await db.commit()


# Update the user's avatar
async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    """
    The update_avatar_url function updates the avatar URL for a user.
    
    :param email: str: Get the user from the database
    :param url: str | None: Specify that the url parameter is either a string or none
    :param db: AsyncSession: Pass the database session into the function
    :return: A user object, which is the updated user
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user


async def get_picture_count(db: AsyncSession, user: User):
    """
    The get_picture_count function retrieves the count of pictures associated with a user and updates the user instance.
    
    :param db: AsyncSession: Inject the database session into the function
    :param user: User: Pass the user instance to the function
    :return: None
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(user=user)
    pictures = await db.execute(stmt)

    if pictures is None:
        picture_count = 1
    else:
        picture_count = len(pictures.unique().all())
    user.picture_count = picture_count
    await db.commit()
    await db.refresh(user)
    
    
async def update_user(email: str, new_email: str, db: AsyncSession):
    """
    The update_user function updates a user's email address.
    
    :param email: str: Identify the user to update
    :param new_email: str: Update the email of the user
    :param db: AsyncSession: Pass in the database session
    :return: A user object
    :doc-author: Trelent
    """
    statement = select(User).filter_by(email=email)
    user = await db.execute(statement)
    user = user.unique().scalar_one_or_none()
    user.email = new_email
    
    await db.commit()
    await db.refresh(user)

    return user


# Comfirm the email of the user
# async def new_password(email: str, new_password:str, db: AsyncSession= Depends(get_db)):
#     """
#     The new_password function takes an email and a new password,
#         then updates the user's password in the database.

#     :param email: str: Get the email of the user who wants to change their password
#     :param new_password:str: Pass in the new password
#     :param db: AsyncSession: Pass the database session into the function
#     :return: The updated user object
#     """
#     user = await get_user_by_email(email, db)
#     user.password = new_password
#     await db.commit()
#     await db.refresh(user)
#     return user
