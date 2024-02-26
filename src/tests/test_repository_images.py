import unittest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.images import (
    get_all_images,
    get_image,
    get_images,
    get_others_image,
    create_image,
    update_image,
    delete_image,
)
from src.entity.models import Image, User, Role
from src.schemas.images import ImageSchema, ImageUpdateSchema
from datetime import datetime


class TestImage(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User()
        self.image = Image(
            id=1,
            image="test",
            user=self.user,
            description="testDEADPOOL",
            created_at=datetime(2000, 3, 12),
            updated_at=datetime(2000, 3, 13),
        )
        self.images = [
            self.image,
            Image(
                id=2,
                image=self.image.image,
                user=self.user,
                description=self.image.description,
                created_at=self.image.created_at,
                updated_at=self.image.updated_at,
            ),
            Image(
                id=3,
                image=self.image.image,
                user=self.user,
                description=self.image.description,
                created_at=self.image.created_at,
                updated_at=self.image.updated_at,
            ),
        ]

    async def test_get_images(self):
        mocked_images = MagicMock()
        self.session.execute.return_value = mocked_images
        mocked_images.scalars.return_value.unique.return_value.all.return_value = (
            self.images
        )
        result = await get_images(10, 0, self.session, User())
        self.assertEqual(result, self.images)

    async def test_get_all_images(self):
        mocked_images = MagicMock()
        self.session.execute.return_value = mocked_images
        mocked_images.scalars.return_value.unique.return_value.all.return_value = (
            self.images
        )
        result = await get_all_images(10, 0, self.session)
        self.assertEqual(result, self.images)

    async def test_get_image(self):
        mocked_image = MagicMock()
        self.session.execute.return_value = mocked_image
        mocked_image.unique.return_value.scalar_one_or_none.return_value = self.image
        result = await get_image(1, self.session, self.user)
        self.assertEqual(result, self.image)

    async def test_create_image(self):
        pass

    async def test_update_image(self):
        pass

    async def test_delete_image(self):
        pass


if __name__ == "__main__":
    unittest.main()
