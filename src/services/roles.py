from fastapi import Request, Depends, HTTPException, status
from src.entity.models import Role, User
from src.services.auth import auth_service


class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
            It takes in two arguments: request and user. The request argument is the Request object, which contains all of
            the information about what was sent by the client (e.g., headers, body). The user argument is a User object that 
            represents who made this request (if they are logged in). This function should return either an HTTPException or 
            None if everything went well.
        
        :param self: Access the class attributes
        :param request: Request: Get the request object
        :param user: User: Get the user object from the auth_service
        :return: A boolean
        :doc-author: Trelent
        """
        print(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )