from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.exceptions import HTTPException
from qrcode import make as making_qr
from src.entity.models import TransformedPic, User, Role, Image
from src.services.cloudconnect import (
    CloudConnect,
    input_error,
)  # our decorator, converts exceptions into httpexceptions


class TransformClass:

    def __init__(self, session: AsyncSession):
        self.session = session  # bind to db

    @input_error
    async def get_original_pic_by_id(self, needed_pic_id: int):
        """
        The get_original_pic_by_id function takes in a picture id and returns the original image object.
            
        
        :param self: Represent the instance of a class
        :param needed_pic_id: int: Get the picture id from the database
        :return: An object of the image class
        :doc-author: Trelent
        """
        query = select(Image).filter(Image.id == needed_pic_id)
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    async def get_trans_pic_by_id(self, needed_pic_id: int):
        """
        The get_trans_pic_by_id function takes in a needed_pic_id and returns the TransformedPic object with that id.
            If no such TransformedPic exists, it returns None.
        
        :param self: Represent the instance of a class
        :param needed_pic_id: int: Specify the id of the picture that is needed
        :return: A transformedpic object, which is a row in the database
        :doc-author: Trelent
        """
        query = select(TransformedPic).filter(TransformedPic.id == needed_pic_id)
        result = await self.session.execute(query)
        return result.unique().scalar_one_or_none()

    @input_error
    async def create_transformed_pic(
        self, user_id: int, original_pic_id: str, transformations: dict
    ):
        """
        The create_transformed_pic function creates a transformed picture from an original picture.
            Args:
                user_id (int): The id of the user who is creating the transformed pic.
                original_pic_id (str): The id of the original pic that will be used to create a new transformed pic.
                transformations (dict): A dictionary containing all transformation parameters for Cloudinary's upload API call, including image format and crop mode.
        
        :param self: Bind the method to an object
        :param user_id: int: Identify the user who uploaded the picture
        :param original_pic_id: str: Get the original picture from the database
        :param transformations: dict: Pass in the transformations that will be applied to the image
        :return: A transformed_pic object, which is an instance of the transformedpic class
        :doc-author: Trelent
        """
        original_pic = await self.get_original_pic_by_id(original_pic_id)
        transformed_pic_url, public_id = await CloudConnect.upload_transformed_pic(
            user_id, original_pic.image, transformations
        )
        transformed_pic = TransformedPic(
            public_id=public_id,
            original_pic_id=original_pic_id,
            url=transformed_pic_url,
            user_id=user_id,
        )
        self.session.add(transformed_pic)
        await self.session.commit()
        await self.session.refresh(transformed_pic)
        return transformed_pic

    @input_error
    async def delete_trans_pic(self, transformed_pic_id: int):
        """
        The delete_trans_pic function deletes a transformed picture from the database and cloud storage.
            Args:
                transformed_pic_id (int): The id of the transformed picture to be deleted.
            Returns: 
                str: A string indicating that the deletion was successful or not.
        
        :param self: Represent the instance of the class
        :param transformed_pic_id: int: Find the picture in the database by its id
        :return: A string
        :doc-author: Trelent
        """
        transformed_pic = await self.get_trans_pic_by_id(transformed_pic_id)
        if transformed_pic:
            await CloudConnect.delete_pic(transformed_pic.public_id)
            await self.session.delete(transformed_pic)
            await self.session.commit()
            return "Successfully deleted"
        return False

    @input_error
    async def get_users_transformed_pic(self, user_id: int):
        """
        The get_users_transformed_pic function returns a list of all the transformed pictures for a given user.
            
        
        :param self: Represent the instance of a class
        :param user_id: int: Get the user_id of the user that is currently logged in
        :return: A list of transformed pictures for a given user
        :doc-author: Trelent
        """
        query = select(TransformedPic).filter(TransformedPic.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().unique().all()

    @input_error
    async def update_transformed_pic(
        self, transformed_pic_id: int, transformations: dict
    ):
        """
        The update_transformed_pic function updates the transformed picture in the database.
            Args:
                self (object): The object that is calling this function.
                transformed_pic_id (int): The id of the picture to be updated.
                transformations (dict): A dictionary containing all of the transformations to be applied to 
                                        this image, as well as their values.
        
        :param self: Refer to the current object
        :param transformed_pic_id: int: Identify the transformed picture that needs to be updated
        :param transformations: dict: Pass in a dictionary of transformations that will be applied to the image
        :return: The transformed_pic object
        :doc-author: Trelent
        """
        transformed_pic = await self.get_trans_pic_by_id(transformed_pic_id)
        if not transformed_pic:
            return None
        new_transformed_url = await CloudConnect.update_pic(
            transformed_pic.public_id, transformations
        )
        transformed_pic.url = new_transformed_url
        self.session.add(transformed_pic)
        await self.session.commit()
        await self.session.refresh(transformed_pic)
        return transformed_pic

    @input_error
    async def generate_qr_code_for_trans(self, trans_pic_id):
        """
        The generate_qr_code_for_trans function generates a QR-code for the given transaction picture.
            The function takes in an integer representing the id of a transaction picture and returns 
            an image object containing the generated QR-code.
        
        :param self: Represent the instance of the class
        :param trans_pic_id: Get the image from the database
        :return: The qr_image
        :doc-author: Trelent
        """
        pic = await self.get_trans_pic_by_id(trans_pic_id)
        if pic:
            qr_image = making_qr(pic.url)
            return qr_image
        raise HTTPException(
            status_code=404, detail="Couldnt generate QR-code, image not found"
        )

    @input_error
    async def check_access(self, pic_id: int, user: User, needed_class):
        """
        The check_access function checks if the user has access to a certain picture.
            It takes in three arguments: pic_id, user and needed_class.
            The pic_id is the id of the picture that we want to check access for.
            The user is an object of type User which contains information about who wants to see this image (the current logged-in user). 
            And finally, needed class can be either Image or TransformedPic depending on what kind of image we are checking access for.
        
        :param self: Represent the instance of a class
        :param pic_id: int: Get the picture by id
        :param user: User: Get the user id and role
        :param needed_class: Check if the user is trying to access an original picture or a transformed one
        :return: True or raises an exception
        :doc-author: Trelent
        """
        if needed_class == Image:
            pic = await self.get_original_pic_by_id(pic_id)
            if not pic:
                raise HTTPException(
                    status_code=404,
                    detail="Picture wasn't found. Are you sure it exists?",
                )
            else:
                if pic.user_id == user.id or user.role == Role.admin:
                    return True
                raise HTTPException(
                    status_code=403, detail="You don't have enough rights!"
                )
        elif needed_class == TransformedPic:
            pic = await self.get_trans_pic_by_id(pic_id)
            if not pic:
                raise HTTPException(
                    status_code=404,
                    detail="Picture wasn't found. Are you sure it exists?",
                )
            else:
                if pic.user_id == user.id or user.role == Role.admin:
                    return True
                raise HTTPException(
                    status_code=403, detail="You don't have enough rights!"
                )
