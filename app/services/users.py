from http import HTTPStatus
from fastapi.responses import JSONResponse
from core.auth import hash_password
from utils.helpers.enums import Status
from repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import  AsyncSession
from schemas.base import UserUpdateData
from fastapi import UploadFile
import shutil
import os
import imghdr


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository


    async def get_all_users(self, db: AsyncSession):
        try:
            user_list = await self.repository.get_all_users(db)
            
            user_list = [user.to_dict() for user in user_list]
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": f"User's list fetched successfully", "user_list": user_list}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )


    async def update_user_status(self, user_id: int, status: Status, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )
            
            await self.repository.update_user_status(user, status, db)
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User status updated successfully"}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def update_user(self, user_id: int, user_update_data: UserUpdateData, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )
            
            if user_update_data.email:
                user_by_email = await self.repository.get_user_by_email(user_update_data.email, db)
                if user_by_email:
                    return JSONResponse(
                        status_code=HTTPStatus.BAD_REQUEST,
                        content={"message": "Email already exists"}
                    )


            if user_update_data.password:
                user_update_data.password = hash_password(user_update_data.password)

            await self.repository.update_user(user_id, user_update_data, db)
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User updated successfully"}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

    async def delete_user(self, user_id: int, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )
            
            await self.repository.delete_user(user_id, db)
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User deleted successfully"}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )
    
    async def get_user(self, user_id: int, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User fetched successfully", "user": user.to_dict()}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )
 
    async def update_user_profile_image(self, user_id: int, file: UploadFile, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)

            if not user:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "User not found"}
                )

            valid_image_types = ['jpeg', 'png', 'gif', 'jpg']
            image_type = imghdr.what(file.file)

            if image_type not in valid_image_types:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "File type not allowed. Only images are accepted."}
                )


            # Ensure directory exists
            upload_dir = "uploads/profile_images"
            os.makedirs(upload_dir, exist_ok=True)

            # save the file with a unique name (e.g., user_id + extension)
            file_extension = file.filename.split(".")[-1]
            file_location = f"{upload_dir}/{user_id}.{file_extension}"

            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Update user profile image in DB
            await self.repository.update_user_profile_image(user, file_location, db)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "User profile image updated successfully", "file_location": file_location}
            )

        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )
