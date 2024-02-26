import unittest
from unittest.mock import AsyncMock, MagicMock
from src.entity.models import User, Comment, Role
from fastapi.exceptions import HTTPException
from src.schemas.comment import CommentCreate
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.comments import create_comment, update_comment, delete_comment


class TestComments(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = AsyncMock(spec=AsyncSession)
        self.user = User(id=1, role=Role.admin)
        self.ordinary_user = User(role=Role.user)
        self.image_id = 4
        self.comment = Comment(
            id=2, comment="testing", image_id=3, user_id=self.user.id
        )

    async def test_create_comment(self):
        body = CommentCreate(comment="test comment")
        result = await create_comment(body, self.session, self.image_id, self.user)
        self.assertEqual(result.comment, body.comment)
        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_update_comment(self):
        mocked_comment = MagicMock()
        self.session.execute.return_value = mocked_comment
        mocked_comment.unique.return_value.scalar_one_or_none.return_value = (
            self.comment
        )
        body = CommentCreate(comment="updating")
        result = await update_comment(self.session, self.comment.id, self.user.id, body)
        self.assertEqual(result.comment, body.comment)
        self.session.add.assert_called_once_with(result)
        self.session.commit.assert_called_once()
        self.session.refresh.assert_called_once_with(result)

    async def test_update_comment_empty(self):
        mocked_comment = MagicMock()
        self.session.execute.return_value = mocked_comment
        mocked_comment.unique.return_value.scalar_one_or_none.return_value = (
            self.comment
        )
        body = CommentCreate(comment="    ")
        result = await update_comment(self.session, self.comment.id, self.user.id, body)
        self.assertIsNone(result)

    async def test_delete_comment(self):
        mocked_comment = MagicMock()
        self.session.execute.return_value = mocked_comment
        mocked_comment.unique.return_value.scalar_one_or_none.return_value = (
            self.comment
        )
        result = await delete_comment(self.session, self.comment.id, self.user.role)
        self.assertEqual(result, self.comment)
        self.session.delete.assert_called_once_with(result)
        self.session.commit.assert_called_once()

    async def test_delete_comment_forbidden(self):
        mocked_comment = MagicMock()
        self.session.execute.return_value = mocked_comment
        mocked_comment.unique.return_value.scalar_one_or_none.return_value = (
            self.comment
        )
        with self.assertRaises(HTTPException):
            await delete_comment(self.session, self.comment.id, self.ordinary_user.role)

    async def test_delete_comment_not_found(self):
        mocked_comment = MagicMock()
        self.session.execute.return_value = mocked_comment
        mocked_comment.unique.return_value.scalar_one_or_none.return_value = None
        with self.assertRaises(HTTPException):
            await delete_comment(self.session, self.comment.id, self.ordinary_user.role)


if __name__ == "__main__":
    unittest.main()
