from fastapi import APIRouter, HTTPException, Depends, status, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import users as repo_users
from src.schemas.users import UserSchema, TokenSchema, UserResponse
from src.services.auth import auth_service
from starlette.responses import JSONResponse
from src.conf import messages

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()


# Use for signup
@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, bt: BackgroundTasks, request: Request, db: AsyncSession = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=messages.ACCOUNT_EXIST)
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repo_users.create_user(body, db)
    # bt.add_task(send_email, new_user.email, new_user.username, str(request.base_url))
    return new_user


# Use for login
@router.post("/login", response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=messages.INVALID_EMAIL)  # sometimes it is better to hide error
    # if not user.status:
    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.EMAIL_NOT_CONFIRMED)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=messages.INVALID_PASSWORD)  # sometimes it is better to hide error
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


# Use for get a refresh token
@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                        db: AsyncSession = Depends(get_db)):
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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.INVALID_REF_TOKEN)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repo_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post('/logout')
async def logout(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token),
                 db: AsyncSession = Depends(get_db)):
    token = credentials.credentials
    print(token)
    email = await auth_service.decode_refresh_token(token)
    print("here is email")
    # print(email)
    user = await repo_users.get_user_by_email(email, db)
    print(user.status)
    if not user.status:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=messages.ALREADY_LOGGED_OUT)

    await repo_users.delete_access_token(email, db)
    return {"message": "Logout Successfully"}