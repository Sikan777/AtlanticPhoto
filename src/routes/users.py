from fastapi import APIRouter, HTTPException, Depends, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.entity.models import User, Role
from src.repository import users as repositories_users
from src.schemas.users import UserResponse, UserUpdate, AnotherUsers
from src.services.auth import auth_service


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    The get_current_user function is a dependency that will be called by FastAPI to get the current user.
    It uses the auth_service.get_current_user function, which we defined above, and also depends on a database session.
    
    :param user: User: Get the current user from the auth_service
    :param db: AsyncSession: Get a database session
    :param : Get the current user from the database
    :return: The current user, which is stored in the database
    :doc-author: Trelent
    """
    await repositories_users.get_picture_count(db, user)
    """
    The get_current_user function is a dependency that will be called by FastAPI to get the current user.
    It uses the auth_service.get_current_user function, which we defined above, and also depends on a database session.
    
    :param user: User: Get the user object from the auth_service
    :param db: AsyncSession: Get a database session
    :param : Get the current user from the database
    :return: The current user, which is stored in the database
    :doc-author: Trelent
    """
    return user


@router.get("/{username}", response_model=UserResponse)
async def get_user_profile(email: str, db: AsyncSession = Depends(get_db)):
    """
    The get_user_profile function is used to get the user profile information.
        This function will return a User object with all of the user's information.
    
    
    :param email: str: Get the email of the user that is logged in
    :param db: AsyncSession: Pass the database session to the repository
    :return: The user_info object, which is a user object
    :doc-author: Trelent
    """
    user_info = await repositories_users.get_user_by_email(email, db)
    await repositories_users.get_picture_count(db, user_info)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user_info


# @router.patch("/me", response_model=UserResponse)
# async def update_own_profile(
#     user_update: UserUpdate,
#     user: User = Depends(auth_service.get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     updated_user = await repositories_users.update_user(
#         user.email, user_update, db
#     )  # Что здесь должно быть? Где метод апдейт юзер?

#     return updated_user


# # маршрут для заборони користувачам лише адмінам
# @router.patch("/admin/{username}/ban")
# async def ban_user(
#     username: str,
#     current_user: User = Depends(auth_service.get_current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     if not current_user.role == Role.admin:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You don't have permission to perform this action, Eshole!",
#         )

#     await repositories_users.ban_user(username, db)  # То же самое, нет метода бан юзер
#     return {"message": f"{username} has been banned."}
