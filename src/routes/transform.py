from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.entity.models import User, TransformedPic, Image
from src.repository.transform import TransformClass
from src.schemas.transform import TransSchema, TransResponse
from src.services.auth import auth_service

# from unittest.mock import MagicMock
from io import BytesIO

# Image = MagicMock()
router = APIRouter(prefix="/transform", tags=["transform"])


@router.post("/create_transformed/{original_image_id}", response_model=TransResponse)
async def create_transformed_pic(
    request: TransSchema,
    original_image_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The create_transformed_pic function is used to create a transformed picture.
        It takes in the original image id, and the transformations that are desired.
        The user must be logged in to use this function.
    
    :param request: TransSchema: Get the transformations from the request body
    :param original_image_id: int: Get the original image from the database
    :param user: User: Get the current user from the database
    :param session: AsyncSession: Get the database session from the dependency injection container
    :param : Get the image id from the url
    :return: A dictionary, but the create_transformed_pic function is used to return a transformedpic object
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    await handler.check_access(
        original_image_id, user, Image
    )  # put mock object, will replace

    trans_pic = await handler.create_transformed_pic(
        user_id=user.id,
        original_pic_id=original_image_id,
        transformations=request.dict(),
    )
    if trans_pic:
        return trans_pic
    raise HTTPException(status_code=404, details="Couldn't transform")


@router.get("/{user_id}/transformed", response_model=List[TransResponse])
async def show_users_transforms(
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The show_users_transforms function returns a list of all the pictures that have been transformed by the user.
        The function takes in an optional parameter, user, which is used to identify which users pictures are being returned.
        If no user is provided then it will return all of the transformed images for every single user.
    
    :param user: User: Get the current user
    :param session: AsyncSession: Connect to the database
    :param : Get the current user that is logged in
    :return: A list of dictionaries
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    result = await handler.get_users_transformed_pic(user.id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Pictures wasn't found")


@router.post("/{transformed_pic_id}/qr")
async def show_qr_code(
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The show_qr_code function is used to generate a QR code for the transformed picture.
        The function takes in the transformed_pic_id and user as parameters, and returns a response object containing
        the generated QR code image.
    
    :param transformed_pic_id: int: Identify the transformed picture that is to be shown
    :param user: User: Get the current user from the database
    :param session: AsyncSession: Get the database session
    :param : Get the transformed picture id from the url
    :return: A response object with the image data of the qr code
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    await handler.check_access(transformed_pic_id, user, TransformedPic)
    qr_image = await handler.generate_qr_code_for_trans(transformed_pic_id)
    with BytesIO() as qr_buffer:
        qr_image.save(qr_buffer, format="PNG")
        qr_buffer.seek(0)
        content_type = "image/png"
        return Response(content=qr_buffer.getvalue(), media_type=content_type)


@router.get("/{transformed_pic_id}", response_model=TransResponse)
async def get_transformed_pic(
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The get_transformed_pic function returns a transformed picture by its id.
        The function checks if the user has access to the picture and then returns it.
    
    :param transformed_pic_id: int: Specify the id of the transformed picture we want to get
    :param user: User: Check if the user has access to the transformed picture
    :param session: AsyncSession: Create a database connection
    :param : Get the transformed picture by id
    :return: A transformed picture by id
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    await handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.get_trans_pic_by_id(transformed_pic_id)
    return result


@router.patch("/{transformed_pic_id}", response_model=TransResponse)
async def update_transformed_pic(
    request: TransSchema,
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The update_transformed_pic function updates a transformed picture in the database.
        It takes an id of the image to be updated, and a request body containing all fields that need updating.
        The function returns the updated image object.
    
    :param request: TransSchema: Get the data from the request body
    :param transformed_pic_id: int: Identify the image to be updated
    :param user: User: Check if the user is authenticated
    :param session: AsyncSession: Pass the database session to the handler class
    :param : Get the id of the transformed picture to be updated
    :return: A dict with the updated transformed_pic
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    await handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.update_transformed_pic(transformed_pic_id, request.dict())
    if result:
        return result
    raise HTTPException(status_code=404, detail="Couldn't update, image not found")


@router.delete("/{transformed_pic_id}")
async def delete_transformed(
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    """
    The delete_transformed function deletes a transformed image from the database.
        It takes in an integer representing the id of the transformed image to be deleted,
        and returns a boolean indicating whether or not it was successful.
    
    :param transformed_pic_id: int: Get the id of the transformed image that we want to delete
    :param user: User: Check if the user has access to delete the transformed picture
    :param session: AsyncSession: Get the database session from the dependency
    :param : Get the id of the image to be deleted
    :return: A bool, which is then used to determine the response
    :doc-author: Trelent
    """
    handler = TransformClass(session)
    await handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.delete_trans_pic(transformed_pic_id)
    if not result:
        raise HTTPException(status_code=404, detail="Couldn't delete, image not found")
