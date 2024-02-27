from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer
)
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.entity.models import User
from src.repository import users as repo_users
from src.schemas.users import UserSchema, TokenSchema, UserResponse
from src.services.auth import auth_service
from starlette.responses import JSONResponse
from src.conf import messages
from jose import JWTError, jwt
import pickle
from src.conf.config import config
import redis

router = APIRouter(prefix="/auth", tags=["auth"])
get_refresh_token = HTTPBearer()
SECRET_KEY = config.SECRET_KEY_JWT
ALGORITHM = config.ALGORITHM
cache = redis.Redis(
        host=config.REDIS_DOMAIN,
        port=config.REDIS_PORT,
        db=0,
        password=config.REDIS_PASSWORD,
    )

# Use for signup
@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def signup(
    body: UserSchema,
    bt: BackgroundTasks,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    The signup function creates a new user in the database.
        It takes a UserSchema object as input, and returns the newly created user.
        If an account with that email already exists, it raises an HTTPException.

    :param body: UserSchema: Validate the request body
    :param bt:BackgroundTasks: Add a task to the background queue
    :param request: Request: Get the base_url of the application
    :param db: AsyncSession: Pass the database session to the function
    :return: A user object
    """
    exist_user = await repo_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST
        )
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repo_users.create_user(body, db)
    # bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


# Use for login
@router.post("/login", response_model=TokenSchema)
async def login(
    body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    """
    The login function is used to authenticate a user.
        It takes in the email and password of the user, verifies that they are correct,
        and then returns an access token for future requests.

    :param body: OAuth2PasswordRequestForm: Get the username and password from the request body
    :param db: AsyncSession: Pass the database session to the function
    :return: A dictionary with the access token, refresh token and the type of token
    """
    user = await repo_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_EMAIL
        )  # sometimes it is better to hide error
    # if not user.status:
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_PASSWORD
        )  # sometimes it is better to hide error
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repo_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
    
#27.02 OAuth2PasswordBearer  auth  
#@router.post("/t_login", response_model=TokenSchema)
async def t_login(
        token: OAuth2PasswordBearer = Depends(), db: AsyncSession = Depends(get_db)
    ):
        """
        The get_current_user function is a dependency that will be used in the
            get_current_active_user endpoint. It takes in a token and db session,
            decodes the JWT, checks if it's an access token or refresh token, then
            returns the user object from cache or database.

        :param self: Access the class attributes
        :param token: str: Get the token from the header
        :param db: AsyncSession: Get the database session
        :return: The user object which is then used to check if the user has access to a certain route
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Decode JWT
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if payload["scope"] == "access_token":
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user_hash = str(email)
        user = cache.get(user_hash)

        if user is None:
            user = await repo_users.get_user_by_email(email, db)
            if user is None:
                raise credentials_exception
            cache.set(user_hash, pickle.dumps(user))
            cache.expire(user_hash, 300)
            # print("User is not from cache")
        else:
            # print("User from cache")
            user = pickle.loads(user)
        return user


# Use for get a refresh token
@router.get("/refresh_token", response_model=TokenSchema)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    """
    The refresh_token function is used to refresh the access token.
        The function takes in a refresh token and returns an access_token,
        a new refresh_token, and the type of token (bearer).

    :param credentials: HTTPAuthorizationCredentials: Get the access token from the header
    :param db: AsyncSession: Get the database session
    :return: A new access token and a new refresh token
    """
    token = credentials.credentials
    print(token)
    email = await auth_service.decode_refresh_token(token)
    print(email)
    user = await repo_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repo_users.update_token(user, None, db)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_REF_TOKEN
        )

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repo_users.update_token(user, refresh_token, db)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
    db: AsyncSession = Depends(get_db),
):
    token = credentials.credentials
    print(token)
    email = await auth_service.decode_refresh_token(token)
    print("here is email")
    # print(email)
    user = await repo_users.get_user_by_email(email, db)
    print(user.status)
    if not user.status:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ALREADY_LOGGED_OUT
        )

    await repo_users.delete_access_token(email, db)
    return {"message": "Logout Successfully"}
