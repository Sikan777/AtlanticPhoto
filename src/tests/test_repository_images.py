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
from src.entity.models import Image, User, Tag
from src.schemas.images import ImageSchema, ImageUpdateSchema
from datetime import datetime
from fastapi.exceptions import HTTPException


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
        self.image_with_tags = ImageSchema(
            description="test tags",
            tags="test1, test2",
        )
        self.too_much_tags = ImageSchema(
            description="test tags",
            tags="test1, test2. test3, test4, test5, test6, test7",
        )

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

    async def test_create_image_without_tags(self):
        body = self.image
        file = "test_image.png"
        result = await create_image(file, body, self.session, self.user)
        self.assertEqual(result.description, body.description)
        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_create_image_with_tags(self):
        body = self.image_with_tags
        file = "test_image.png"
        mocked_tag = MagicMock()
        self.session.execute.return_value = mocked_tag
        mocked_tag.scalar_one_or_none.return_value = None
        result = await create_image(file, body, self.session, self.user)
        self.assertEqual(result.description, body.description)
        self.assertIsNotNone(result.tags)
        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_create_image_too_much_tags(self):
        body = self.too_much_tags
        file = "test_image.png"
        with self.assertRaises(HTTPException):
            await create_image(file, body, self.session, self.user)

    async def test_update_image(self):
        mocked_pic = MagicMock()
        self.session.execute.return_value = mocked_pic
        mocked_pic.unique.return_value.scalar_one_or_none.return_value = self.image
        result = await update_image(
            self.image.id, self.image_with_tags, self.session, self.user
        )
        self.assertEqual(result.description, self.image_with_tags.description)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_delete_image(self):
        mocked_pic = MagicMock()
        self.session.execute.return_value = mocked_pic
        mocked_pic.unique.return_value.scalar_one_or_none.return_value = self.image
        result = await delete_image(self.image.id, self.session, self.user)
        self.assertIsNone(result, "Pic was not deleted")
        self.session.delete.assert_called_once_with(self.image)
        self.session.commit.assert_called_once()

    async def test_delete_image_forbidden(self):
        mocked_pic = MagicMock()
        self.session.execute.return_value = mocked_pic
        mocked_pic.unique.return_value.scalar_one_or_none.return_value = self.image
        with self.assertRaises(HTTPException):
            await delete_image(self.image.id, self.session, User(id=4))

    async def test_delete_image_not_found(self):
        mocked_pic = MagicMock()
        self.session.execute.return_value = mocked_pic
        mocked_pic.unique.return_value.scalar_one_or_none.return_value = None
        with self.assertRaises(HTTPException):
            await delete_image(self.image.id, self.session, self.user)


if __name__ == "__main__":
    unittest.main()
