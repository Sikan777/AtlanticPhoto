from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from qrcode import make as making_qr
from src.entity.models import TransformedPic, User, Role, Image
from src.services.cloudconnect import (
    CloudConnect,
    input_error,
)  # our decorator, converts exceptions into httpexceptions


class TransformClass:

    def __init__(self, session: AsyncSession):
        self.session = session  # bind to db

    @input_error
    async def get_original_pic_by_id(self, needed_pic_id: int):
        query = select(Image).filter(Image.id == needed_pic_id)
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_trans_pic_by_id(self, needed_pic_id: int):
        query = select(TransformedPic).filter(TransformedPic.id == needed_pic_id)
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    @input_error
    async def create_transformed_pic(
        self, user_id: int, original_pic_id: str, transformations: dict
    ):
        original_pic = await self.get_original_pic_by_id(original_pic_id)
        transformed_pic_url, public_id = await CloudConnect.upload_transformed_pic(
            user_id, original_pic.image, transformations
        )
        transformed_pic = TransformedPic(
            public_id=public_id,
            original_pic_id=original_pic_id,
            url=transformed_pic_url,
            user_id=user_id,
        )
        self.session.add(transformed_pic)
        await self.session.commit()
        await self.session.refresh(transformed_pic)
        return transformed_pic

    @input_error
    async def delete_trans_pic(self, transformed_pic_id: int):
        transformed_pic = await self.get_trans_pic_by_id(transformed_pic_id)
        if transformed_pic:
            await CloudConnect.delete_pic(transformed_pic.public_id)
            await self.session.delete(transformed_pic)
            await self.session.commit()
            return "Successfully deleted"
        return False

    @input_error
    async def get_users_transformed_pic(self, user_id: int):
        query = select(TransformedPic).filter(TransformedPic.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    @input_error
    async def update_transformed_pic(
        self, transformed_pic_id: int, transformations: dict
    ):
        transformed_pic = await self.get_trans_pic_by_id(transformed_pic_id)
        if not transformed_pic:
            return None
        new_transformed_url = await CloudConnect.update_pic(
            transformed_pic.public_id, transformations
        )
        transformed_pic.url = new_transformed_url
        self.session.add(transformed_pic)
        await self.session.commit()
        await self.session.refresh(transformed_pic)
        return transformed_pic

    @input_error
    async def generate_qr_code_for_trans(self, trans_pic_id):
        pic = await self.get_trans_pic_by_id(trans_pic_id)
        if pic:
            qr_image = making_qr(pic.url)
            return qr_image
        raise HTTPException(
            status_code=404, detail="Couldnt generate QR-code, image not found"
        )

    @input_error
    async def check_access(self, pic_id: int, user: User, needed_class):
        if needed_class == Image:
            pic = await self.get_original_pic_by_id(pic_id)
            if not pic:
                raise HTTPException(
                    status_code=404,
                    detail="Picture wasn't found. Are you sure it exists?",
                )
            else:
                if pic.user_id == user.id or user.role == Role.admin:
                    return True
                raise HTTPException(
                    status_code=403, detail="You don't have enough rights!"
                )
        elif needed_class == TransformedPic:
            pic = await self.get_trans_pic_by_id(pic_id)
            if not pic:
                raise HTTPException(
                    status_code=404,
                    detail="Picture wasn't found. Are you sure it exists?",
                )
            else:
                if pic.user_id == user.id or user.role == Role.admin:
                    return True
                raise HTTPException(
                    status_code=403, detail="You don't have enough rights!"
                )
