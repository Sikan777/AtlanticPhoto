from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from unittest.mock import MagicMock  # temporary
from qrcode import make as making_qr
from src.entity.models import TransformedPic, User, Role
from src.services.cloudconnect import CloudConnect, input_error  # our decorator, converts exceptions into httpexceptions

Image = MagicMock()  # temporary


class TransformClass:

    def __init__(self, session: AsyncSession):
        self.session = session  # bind to db

    @input_error
    async def get_pic_by_id(self, needed_pic_id: int, needed_class):
        query = select(needed_class).filter(needed_class.id == needed_pic_id)
        result = await self.session.execute(query)
        return result.unique().first()

    @input_error
    async def create_transformed_pic(
        self, user_id: int, original_pic_id: str, transformations: dict
    ):
        original_pic = await self.get_pic_by_id(original_pic_id, Image)
        transformed_pic_url, public_id = await CloudConnect.upload_transformed_pic(
            user_id, original_pic.url, transformations
        )
        transformed_pic = TransformedPic(
            public_id=public_id,
            # original_pic_id=original_pic_id,
            url=transformed_pic_url,
            user_id=user_id,
        )
        self.session.add(transformed_pic)
        await self.session.commit()
        await self.session.refresh(transformed_pic)
        return transformed_pic

    @input_error
    async def delete_trans_pic(self, transformed_pic_id: int):
        transformed_pic = await self.get_pic_by_id(transformed_pic_id, TransformedPic)
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
        transformed_pic = await self.get_pic_by_id(transformed_pic_id, TransformedPic)
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
        pic = await self.get_pic_by_id(trans_pic_id, TransformedPic)
        if pic:
            qr_image = making_qr(pic.url)
            return qr_image
        raise Exception("Couldnt generate QR-code")

    @input_error
    async def check_access(self, pic_id: int, user: User, needed_class):
        pic = await self.get_pic_by_id(pic_id, needed_class)
        if pic:
            if pic.user_id != user.id or user.role != Role.admin:
                raise Exception("You don't have enough right!")
        raise Exception("Picture wasn't found. Are you sure it exists?")