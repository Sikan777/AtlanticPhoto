from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from fastapi import UploadFile
from src.entity.models import Image, User, Role
from src.schemas.images import ImageSchema, ImageUpdateSchema
from fastapi import UploadFile, HTTPException, status
from src.repository.tags import create_tag
from src.repository.users import get_user_by_email


# this is used to get all images per User
async def get_images(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_images function returns a list of images for the user.

    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the number of images to skip
    :param db: AsyncSession: Pass the database connection to the function
    :param user: User: Filter the images by user
    :return: A list of images for the user
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(user=user).offset(offset).limit(limit)
    images = await db.execute(stmt)
    return images.scalars().unique().all()


# this is used to get all contacts
async def get_all_images(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_images function returns a list of all images in the database.

    :param limit: int: Limit the number of images returned
    :param offset: int: Specify the number of records to skip
    :param db: AsyncSession: Pass in the database session
    :return: A list of all images in the database
    :doc-author: Trelent
    """
    stmt = select(Image).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().unique().all()


# this is used to get only 1 image by the id
async def get_image(image_id: int, db: AsyncSession, user: User):
    """
    The get_image function takes in an image_id and a user, and returns the image with that id if it exists.
            If no such image exists, None is returned.

    :param image_id: int: Specify the image id of the image we want to retrieve
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user from the database
    :return: An image object, which is the result of a sqlalchemy query
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(id=image_id)
    response = await db.execute(stmt)
    image = response.unique().scalar_one_or_none()
    if image.user == user or user.role == Role.admin:
        return image
    raise HTTPException(status_code=403, detail="Access forbidden")


async def get_others_image(image_id: int, db: AsyncSession, user: User):
    """
    The get_others_image function takes in an image_id and a user, and returns the image with that id if it exists.
            If no such image exists, None is returned.

    :param image_id: int: Specify the image id of the image we want to retrieve
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user from the database
    :return: An image object, which is the result of a sqlalchemy query
    :doc-author: Trelent
    """
    stmt = select(Image).filter_by(id=image_id)
    image = await db.execute(stmt)
    if image and get_user_by_email(user.email):
        return image.unique().scalar_one_or_none()


def is_object_added(session: AsyncSession, obj):
    """
    The is_object_added function checks if an object is already added to the session.

    :param session: AsyncSession: Pass in the session object
    :param obj: Check if the object is added to the session
    :return: True if the object is added to the session, false otherwise
    :doc-author: Trelent
    """
    return session.is_modified(obj, include_collections=False)


# this is used to create one new image
async def create_image(file: str, body: ImageSchema, db: AsyncSession, user: User):
    """
    The create_image function creates a new image in the database.

    :param file: str: Pass the file name to the function
    :param body: ImageSchema: Validate the request body
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user id from the token
    :return: A new image object
    :doc-author: Trelent
    """
    # image = Image(**body.model_dump(exclude_unset=True), user=user)
    tags_l = []
    if body.tags:
        tags = [tag.strip() for tag in body.tags.split(",")]
        if len(tags) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Too many tags"
            )
        for tag in tags:
            tag = await create_tag(tag, db, user)
            tags_l.append(tag)
        image = Image(description=body.description, image=file, user=user, tags=tags_l)
    else:
        image = Image(description=body.description, image=file, user=user)
    if not is_object_added(db, image):
        db.add(image)
    image = await db.merge(image, load=True)
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
    stmt = select(Image).filter_by(id=image_id)
    response = await db.execute(stmt)
    image = response.unique().scalar_one_or_none()
    if image.user == user or user.role == Role.admin:
        image.description = body.description
        await db.commit()
        await db.refresh(image)
        return image
    raise HTTPException(status_code=403, detail="Access forbidden")


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
    stmt = select(Image).filter_by(id=image_id)
    response = await db.execute(stmt)
    image = response.unique().scalar_one_or_none()
    if image:
        if image.user == user or user.role == Role.admin:
            await db.delete(image)
            await db.commit()
            return None
        raise HTTPException(status_code=403, detail="Access forbidden")
    raise HTTPException(status_code=404, detail="Image doesn't exist")
