import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import User, TransformedPic, Image
from src.repository.transform import TransformClass
from src.services.cloudconnect import CloudConnect
from datetime import datetime


class TestTrans(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.transform_class = TransformClass(self.session)
        self.user = User()
        self.image = Image(
            id=1,
            image="test",
            user=self.user,
            description="testDEADPOOL",
            created_at=datetime(2000, 3, 12),
            updated_at=datetime(2000, 3, 13),
        )

    async def test_get_original_pic_by_id(self):
        mocked_pic = MagicMock()
        self.session.execute.return_value = mocked_pic
        mocked_pic.unique.return_value.scalar_one_or_none.return_value = self.image
        result = await self.transform_class.get_original_pic_by_id(self.image.id)
        self.assertEqual(result.id, self.image.id)

    async def test_get_trans_pic_by_id(self):
        pass

    async def test_create_transformed_pic(self):
        pass

    async def test_update_trans_pic(self):
        pass

    async def test_delete_trans_pic(self):
        pass

    async def test_generate_qr_code_for_trans(self):
        pass


if __name__ == "__main__":
    unittest.main()
