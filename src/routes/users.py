import statistics
from fastapi import APIRouter, Depends, HTTPException
from src.database.db import get_db
from src.services.auth import auth_service
from src.entity.models import User
from src.repository import users as repo_users

from src.schemas.users import UserResponse
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/users', tags=['auth'])


#additional task 1
@router.get("/profile/{username}", response_model=UserResponse)
async def get_user_profile(username: str, db: AsyncSession = Depends(get_db)):
    """
    Получение профиля пользователя по его уникальному username.

    :param username: str: Уникальное имя пользователя
    :param db: AsyncSession: Сессия базы данных
    :return: UserProfileResponse: Информация о профиле пользователя
    """
    user = await repo_users.get_user_by_username(username, db)
    if user is None:
        raise HTTPException(status_code=statistics.HTTP_404_NOT_FOUND, detail="User not found")
    # Здесь можно добавить логику для получения другой информации о пользователе, такой как количество загруженных фотографий и т. д.
    # Например:
    # photos_count = await repo_photos.get_photos_count_by_user_id(user.id, db)
    # Затем добавить это значение возвращаемого объекта.
    return user