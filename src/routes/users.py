from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role
from src.repository import users as repositories_users
from src.schemas.users import UserResponse, UserUpdate, AnotherUsers
from src.services.auth import auth_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)):
    await repositories_users.get_picture_count(db, user)
    return user


@router.get("/{username}", response_model=AnotherUsers)
async def get_user_profile(username: str, db: AsyncSession = Depends(get_db)):
    user_info = await repositories_users.get_user_by_username(username, db)
    await repositories_users.get_picture_count(db, user_info)

    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    return user_info


@router.patch("/me", response_model=UserResponse)
async def update_own_profile(
        user_update: UserUpdate,
        user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    updated_user = await repositories_users.update_user(user.email, user_update, db)

    return updated_user

#маршрут для заборони користувачам лише адмінам
@router.patch("/admin/{username}/ban")
async def ban_user(
        username: str,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    if not current_user.role == Role.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to perform this action.",
        )

    await repositories_users.ban_user(username, db)
    return {"message": f"{username} has been banned."}