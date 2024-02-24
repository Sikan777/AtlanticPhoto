from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from fastapi import UploadFile
from src.entity.models import Image, User
from src.schemas.images import ImageSchema, ImageUpdateSchema


# this is used to get all images per User
async def get_images(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_images function returns a list of images for the user.

    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the number of images to skip
    :param db: AsyncSession: Pass the database connection to the function
    :param user:User: Filter the images by user
    :return: A list of images
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(user=user).offset(offset).limit(limit)
    images = await db.execute(stmt)
    return images.scalars().all()


# this is used to get all contacts
async def get_all_images(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_images function returns a list of all images in the database.


    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass in the database session
    :return: All the images in the database
    :doc-author: Trelent
    """
    stmt = select(Image).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


# this is used to get only 1 image by the id
async def get_image(image_id: int, db: AsyncSession, user: User):
    """
    The get_image function takes in an image_id and a user, and returns the image with that id if it exists.
        If no such image exists, None is returned.

    :param image_id: int: Specify the image id of the image we want to retrieve
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Get the user from the database
    :return: An image object, which is the result of a sqlalchemy query
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(id=image_id, user=user)
    image = await db.execute(stmt)
    return image.unique().scalar_one_or_none()


# this is used to create one new image
async def create_image(file: str, body: ImageSchema, db: AsyncSession, user: User):
    """
    The create_image function creates a new image in the database.

    :param body: ImageSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Get the user id from the token
    :return: An image object
    :doc-author: Trelent
    """
    # image = Image(**body.model_dump(exclude_unset=True), user=user)
    image = Image(description=body.description, image=file, user=user)
    db.add(image)
    await db.commit()
    await db.refresh(image)
    return image


# this is used to update an image
async def update_image(
    image_id: int, body: ImageUpdateSchema, db: AsyncSession, user: User
):
    """
    The update_image function updates the description of an image.

    :param image_id: int: Specify the id of the image to be updated
    :param body: ImageUpdateSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Ensure that the user is only able to update their own images
    :return: A single image
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(id=image_id, user=user)
    result = await db.execute(stmt)
    image = result.scalar_one_or_none()
    if image:
        image.description = body.description
        await db.commit()
        await db.refresh(image)
    return image


# this is used to delete existed image by the id
async def delete_image(image_id: int, db: AsyncSession, user: User):
    """
    The delete_image function deletes an image from the database.

    :param image_id: int: Specify the image that is to be deleted
    :param db: AsyncSession: Pass the database session to the function
    :param user:User: Check if the user is allowed to delete the image
    :return: The image that was deleted
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(id=image_id, user=user)
    image = await db.execute(stmt)
    image = image.scalar_one_or_none()
    if image:
        await db.delete(image)
        await db.commit()
    return image
