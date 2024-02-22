from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.entity.models import User, TransformedPic
from src.repository.transform import TransformClass
from src.schemas.transform import TransSchema, TransResponse
from src.services.auth import auth_service
from unittest.mock import MagicMock  # temporary
from io import BytesIO

router = APIRouter(prefix="/transform", tags=["auth"])
Image = MagicMock()  # temporary


@router.post("/create_transformed/{original_image_id}", response_model=TransResponse)
async def create_transformed_pic(
    request: TransSchema,
    original_image_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    handler = TransformClass(session)
    handler.check_access(
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
    handler = TransformClass(session)
    result = await handler.get_users_transformed_pic(user.id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Pictures aren't found")


@router.post("/{transformed_pic_id}/qr")
async def show_qr_code(
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    handler = TransformClass(session)
    handler.check_access(transformed_pic_id, user, TransformedPic)
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
    handler = TransformClass(session)
    handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.get_pic_by_id(transformed_pic_id, TransformedPic)
    return result


@router.patch("/{transformed_pic_id}", response_model=TransResponse)
async def update_transformed_pic(
    request: TransSchema,
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    handler = TransformClass(session)
    handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.update_transformed_pic(transformed_pic_id, request.dict())
    if result:
        return result
    raise HTTPException(status_code=404, detail="Couldn't update")


@router.delete("/{transformed_pic_id}")
async def delete_transformed(
    transformed_pic_id: int,
    user: User = Depends(auth_service.get_current_user),
    session: AsyncSession = Depends(get_db),
):
    handler = TransformClass(session)
    handler.check_access(transformed_pic_id, user, TransformedPic)
    result = await handler.delete_trans_pic(transformed_pic_id)
    if not result:
        raise HTTPException(status_code=404, detail="Couldn't delete")