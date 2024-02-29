import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.entity.models import User, Role
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
        body = UserSchema(username="test_user", email="user@i.com", password="1234567")
        mocked_user = AsyncMock()
        self.session.execute.return_value.func.count.return_value = mocked_user
        mocked_user.scalar.return_value = 0
        mock_gravatar_instance = MockGravatar.return_value
        mock_gravatar_instance.get_image.return_value = "http://some_avatar.ua"
        result = await create_user(body, self.session)
        self.assertIsNotNone(result)
        # self.assertEqual(result.role)
        # self.session.add.assert_called_once_with(result)
        # self.session.commit.assert_called_once()
        # self.session.refresh.assert_called_once_with(result)

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
