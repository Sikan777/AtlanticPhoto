# router = APIRouter(prefix='/images', tags=['auth'])
from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.db import get_db
from src.repository import images as repo_images
from src.schemas.images import ImageResponse, ImageSchema, ImageUpdateSchema
from src.services.auth import auth_service
from src.entity.models import User, Role
from src.services.roles import RoleAccess
from fastapi_limiter.depends import RateLimiter
from fastapi import UploadFile, File
import cloudinary
import cloudinary.uploader
from src.conf.config import config

router = APIRouter(prefix="/images", tags=["images"])

cloudinary.config(
    cloud_name=config.CLD_NAME,
    api_key=config.CLD_API_KEY,
    api_secret=config.CLD_API_SECRET,
    secure=True,
)

access_to_route_all = RoleAccess([Role.admin, Role.moderator])


# this is used to get all contacts - for user
@router.get(
    "/",
    response_model=list[ImageResponse],
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_images(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_images function returns a list of images.

    :param limit: int: Limit the number of images returned
    :param ge: Set a minimum value for the limit parameter
    :param le: Limit the maximum number of images that can be returned
    :param offset: int: Specify the offset of the images to be returned
    :param ge: Set a lower limit on the value of the parameter
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the current user from the database
    :return: A list of images with the following fields:
    :doc-author: Trelent
    """
    images = await repo_images.get_images(limit, offset, db, current_user)
    return images


# insert checking to othersalembic init


# this function is used to get all contacts
@router.get(
    "/all",
    response_model=list[ImageResponse],
    dependencies=[Depends(access_to_route_all)],
)
async def get_all_images(
    limit: int = Query(10, ge=10, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """
    The get_all_images function returns a list of all images in the database.
        The limit and offset parameters are used to paginate the results.


    :param limit: int: Limit the number of images returned
    :param ge: Set a minimum value for the limit parameter
    :param le: Limit the number of images returned to 500
    :param offset: int: Skip a number of images
    :param ge: Specify the minimum value of the parameter
    :param db: AsyncSession: Access the database
    :param user: User: Get the current user
    :return: A list of images
    :doc-author: Trelent
    """
    images = await repo_images.get_all_images(limit, offset, db)  # TODO create funtion
    return images


# this is used to get only 1 image by the id
@router.get(
    "/{image_id}",
    response_model=ImageResponse,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def get_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_image function returns a contact by ID.

    :param image_id: int: Get the image id from the url
    :param db: AsyncSession: Pass the database session to the function
    :param current_user:User: Get the current user from the database
    :return: A contact object
    :doc-author: Trelent
    """
    image = await repo_images.get_image(image_id, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return image


# this is used to create one new image
@router.post(
    "/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def create_image(
    file: UploadFile = File(),
    body: ImageSchema = Depends(ImageSchema),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The create_image function creates a new image in the database.
        The function takes an ImageSchema object as input, and returns an ImageResponse object.


    :param body: ImageSchema: Validate the request body
    :param db: AsyncSession: Get the database session
    :param current_user:User: Get the current user from the database
    :return: An image object
    :doc-author: Trelent
    """
    print(body)
    public_id = f"Image/{current_user.email}"
    res = cloudinary.uploader.upload(file.file, public_id=public_id, owerite=True)
    # print(res)
    res_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250, height=250, crop="fill", version=res.get("version")
    )
    image = await repo_images.create_image(res_url, body, db, current_user)
    return image


# this is used to update existed contact
@router.patch("/{image_id}", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def update_image(
    body: ImageUpdateSchema,
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_image function updates an image in the database.
        It takes a contact_id and body as input, and returns the updated image.


    :param body: ImageUpdateSchema: Get the data from the request body
    :param contact_id: int: Specify the contact id of the image that is to be deleted
    :param db: AsyncSession: Get the database connection
    :param current_user:User: Get the current user from the auth_service
    :return: The updated image
    :doc-author: Trelent
    """
    image = await repo_images.update_image(image_id, body, db, current_user)
    if image is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return image


# this is used to delete existed contact by the id
@router.delete(
    "/{image_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(RateLimiter(times=10, seconds=60))],
)
async def delete_image(
    image_id: int = Path(ge=1),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The delete_image function deletes an image from the database.
        The function takes in a Path parameter of image_id, which is the id of the image to be deleted.
        It also takes in a Depends parameter db, which is an AsyncSession object that allows us to access our database.
        Finally it takes in another Depends parameter current_user, which is a User object representing who made this request.

    :param image_id: int: Get the image id from the path
    :param db: AsyncSession: Pass the database session to the function
    :param current_user:User: Get the user that is currently logged in
    :return: A dict with the following keys:
    :doc-author: Trelent
    """
    image = await repo_images.delete_image(image_id, db, current_user)
    return image
