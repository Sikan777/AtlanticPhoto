import unittest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import Tag, User, Image
from src.schemas.tags import TagSchema
from src.repository.tags import get_tag, get_tag_by_name, create_tag, remove_tag


class TestTag(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.tag = Tag(id=1, name="testtag", user_id=2)

    async def test_get_tag(self):
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = self.tag
        self.session.execute.return_value = mocked_tag
        result = await get_tag(1, self.session, User())
        self.assertIsNotNone(result, "Tag object is None")

    async def test_get_tag_by_name(self):
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = self.tag
        self.session.execute.return_value = mocked_tag
        result = await get_tag_by_name(self.session, self.tag.name)
        self.assertIsNotNone(result, "Tag object is None")

    async def test_create_tag(self):
        body = TagSchema(name="newtag")
        mocked_tag = MagicMock()
        mocked_tag.scalar_one_or_none.return_value = self.tag
        self.session.execute.return_value = mocked_tag
        result = await create_tag(body, self.session, User())
        self.assertIsNotNone(result, "Tag was not created")

    async def test_remove_tag(self):
        mocked_tag = MagicMock(id=1)
        mocked_tag.unique.return_value.scalar_one_or_none.return_value = mocked_tag
        self.session.execute.return_value = mocked_tag
        result = await remove_tag(1, self.session, User())
        self.assertEqual(result, mocked_tag)


if __name__ == "__main__":
    unittest.main()
