import unittest
from unittest.mock import patch, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import User
from src.repository.users import create_user, update_token, update_avatar_url
from src.schemas.users import UserSchema

class TestUser(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(
            id=1, username="test_user", password="qwerty", email="test@example.com"
        )

    @patch("src.repository.users.Gravatar")
    async def test_create_user_success(self, MockGravatar):
        pass

    async def test_create_user_failed(self):
        pass

    async def test_update_avatar_url(self):
        pass

    async def test_get_picture_count(self):
        pass

    async def test_update_token(self):
        pass


if __name__ == "__main__":
    unittest.main()
