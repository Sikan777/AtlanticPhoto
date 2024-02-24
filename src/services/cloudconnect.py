from cloudinary import config
import cloudinary.uploader as uploading
from cloudinary.exceptions import Error
from fastapi import HTTPException, UploadFile
from requests.exceptions import RequestException
from src.conf.config import config as con

# from PIL import Image
from functools import wraps

config(
    cloud_name=con.CLD_NAME,
    api_key=con.CLD_API_KEY,
    api_secret=con.CLD_API_SECRET,
)


# It`s a decorator that copes with exceptions
def input_error(func):
    """
    The input_error function is a decorator that wraps the function it's applied to.
    It catches any exceptions raised by the wrapped function and raises an HTTPException instead.
    This allows us to return a more helpful error message than just &quot;Internal Server Error&quot;.

    :param func: Pass the function that is being decorated
    :return: A wrapper function
    :doc-author: Trelent
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        The wrapper function is a decorator that catches any exceptions thrown by the decorated function and raises an HTTPException with a status code of 500.

        :param *args: Send a non-keyworded variable length argument list to the function
        :param **kwargs: Pass keyworded, variable-length argument list to a function
        :return: A function
        :doc-author: Trelent
        """
        try:
            return func(*args, **kwargs)
        except RequestException as e:
            raise HTTPException(status_code=500, detail=f"Network error: {e}")
        except Error as e:
            raise HTTPException(status_code=500, detail=f"Cloudinary error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong: {e}")

    return wrapper


def create_folder(user_id: int, related_path: str, folder: str = None):
    """
    The create_folder function creates a folder in the user's Google Drive account.
        Args:
            user_id (int): The ID of the user whose Google Drive account will be used to create a folder.
            related_path (str): A string representing the path to which this new folder will be created relative to
                AtlanticPhoto/user_{user_id}. For example, if you want your new folder created at
                AtlanticPhoto/user_{user_id}/photos, then related_path should equal &quot;photos&quot;. If you want your new
                folder created at AtlanticPhoto/user_{

    :param user_id: int: Specify the user for whom a folder will be created
    :param related_path: str: Create a folder path
    :param folder: str: Create a folder path
    :return: A string
    :doc-author: Trelent
    """
    if not folder:
        folder = f"AtlanticPhoto/user_{user_id}/{related_path}"
        return folder
    return folder


class CloudConnect:

    @staticmethod
    @input_error
    async def upload_pic(user_id: int, image: UploadFile, folder: str = None):
        """
        The upload_pic function takes in a user_id, an image file, and an optional folder name.
        If no folder is specified, the function will create a new one with the format &quot;AtlanticPhoto/user_{user_id}/images&quot;.
        The function then uploads the image to Cloudinary using their Python SDK. The result of this upload is returned as a dictionary containing two keys: url and public_id.

        :param user_id: int: Specify the user_id of the user who is uploading a picture
        :param image: UploadFile: Upload the image to cloudinary
        :param folder: str: Specify the folder where the image will be uploaded to
        :return: A tuple of the url and public_id
        :doc-author: Trelent
        """
        folder = create_folder(user_id, "images", folder)
        result = uploading.upload(image.file, folder=folder)
        return result["url"], result["public_id"]

    @staticmethod
    @input_error
    async def upload_transformed_pic(
        user_id: int, original_url: str, transformations: dict, folder: str = None
    ):
        """
        The upload_transformed_pic function takes in a user_id, transform_url, transformations and folder.
        The function then uploads the transformed image to Cloudinary using the uploading.upload function from cloudinary.uploader
        and returns a url and public id for that image.

        :param user_id: int: Specify the user id of the person who is uploading a photo
        :param original_url: str: Pass the url of the image to be transformed
        :param transformations: dict: Apply transformations to the image
        :param folder: str: Specify the folder where the transformed image will be stored
        :return: A tuple of two values: the image url and the public id
        :doc-author: Trelent
        """

        folder = create_folder(user_id, "transformed_images", folder)
        result = uploading.upload(
            original_url, transformations=transformations, folder=folder
        )
        return result["url"], result["public_id"]

    @staticmethod
    @input_error
    async def delete_pic(pic_public_id: str):
        """
        The delete_pic function deletes a picture from the cloudinary database.
            Args:
                pic_public_id (str): The public id of the picture to be deleted.


        :param pic_public_id: str: Specify the public id of the picture that is to be deleted
        :return: The response from the destroy method
        :doc-author: Trelent
        """
        uploading.destroy(public_id=pic_public_id)

    @staticmethod
    @input_error
    async def update_pic(public_id: int, transformations: dict):
        """
        The update_pic function takes a public_id and transformations dict as arguments.
        The function then calls the Cloudinary API to update the image with the given public_id,
        using the transformations provided in the transformations dict. The function returns a url for
        the updated image.

        :param public_id: int: Specify the public id of the image to be updated
        :param transformations: dict: Apply transformations to the image
        :return: The url of the new image
        :doc-author: Trelent
        """
        result = uploading.explicit(public_id, type="upload", eager=[transformations])
        return result["url"]
