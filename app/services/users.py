from http import HTTPStatus
from repository.department_repository import DepartmentRepository
from repository.service_profile_repository import ServiceProfileRepository
from repository.user_document_repository import UserDocumentRepository
from utils.helpers.file_handler import get_base64_file
from core.auth import hash_password
from utils.helpers.enums import Status
from repository.user_repository import UserRepository
from sqlalchemy.ext.asyncio import  AsyncSession
from schemas.base import UserUpdateData
from fastapi import UploadFile
import shutil
import os
import imghdr
from utils.helpers.response_handler import CustomResponseHandler



class UserService:
    def __init__(self, repository: UserRepository, service_profile_repository: ServiceProfileRepository, user_document_repository: UserDocumentRepository, department_repository: DepartmentRepository):
        self.repository = repository
        self.service_profile_repository = service_profile_repository
        self.user_document_repository = user_document_repository
        self.department_repository = department_repository


    async def get_all_users(self, db: AsyncSession):
        try:
            user_list = await self.repository.get_all_users(db)
            
            user_list = [user.to_dict() for user in user_list]
            
            return CustomResponseHandler.success(
                message=f"User's list fetched successfully",
                data={"user_list": user_list},
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )


    async def update_user_status(self, user_id: int, status: Status, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return CustomResponseHandler.error(
                    message="User not found",
                    status_code=HTTPStatus.NOT_FOUND
                )
            
            await self.repository.update_user_status(user, status, db)
            
            return CustomResponseHandler.success(
                message="User status updated successfully",
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    async def update_user(self, user_id: int, user_update_data: UserUpdateData, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            if not user:
                return CustomResponseHandler.error(
                    message="User not found",
                    status_code=HTTPStatus.NOT_FOUND
                )
            
            if user_update_data.email:
                user_by_email = await self.repository.get_user_by_email(user_update_data.email, db)
                if user_by_email:
                    return CustomResponseHandler.error(
                        message="Email already exists",
                        status_code=HTTPStatus.BAD_REQUEST
                    )


            if user_update_data.password:
                user_update_data.password = hash_password(user_update_data.password)

            await self.repository.update_user(user_id, user_update_data, db)
            
            return CustomResponseHandler.success(
                message="User updated successfully",
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    async def delete_user(self, user_id: int, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return CustomResponseHandler.error(
                    message="User not found",
                    status_code=HTTPStatus.NOT_FOUND
                )
            
            await self.repository.delete_user(user_id, db)
            
            return CustomResponseHandler.success(
                message="User deleted successfully",
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
    
    async def get_user(self, user_id: int, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)
            
            if not user:
                return CustomResponseHandler.error(
                    message="User not found",
                    status_code=HTTPStatus.NOT_FOUND
                )
            
            existing_service_profile, platform_type = await self.service_profile_repository.get_service_profile_by_user_id(user_id, db)
            
            if not existing_service_profile:
                return CustomResponseHandler.success(
                    message="User fetched successfully",
                    data={"user": user.to_dict(), "service_profile": None, "document_list": None},
                    status_code=HTTPStatus.OK
                )
            
            document_list = await self.user_document_repository.get_user_documents_by_ids(existing_service_profile.document_id_list, db)
            formatted_documents = [
                get_base64_file(doc.file_name) for doc in document_list
            ]
            
            department = await self.department_repository.get_department_by_id_and_platform_type(existing_service_profile.department_id, platform_type, db)
            
            service_profile_dict = existing_service_profile.to_dict()
            service_profile_dict.pop('document_id_list', None)
            service_profile_dict['department_name'] = department.name
            
            return CustomResponseHandler.success(
                message="User fetched successfully",
                data={"user": user.to_dict(), "service_profile": service_profile_dict, "document_list": formatted_documents},
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    async def update_user_profile_image(self, user_id: int, file: UploadFile, db: AsyncSession):
        try:
            user = await self.repository.get_user_by_user_id(user_id, db)

            if not user:
                return CustomResponseHandler.error(
                    message="User not found",
                    status_code=HTTPStatus.NOT_FOUND
                )

            valid_image_types = ['jpeg', 'png', 'gif', 'jpg']
            image_type = imghdr.what(file.file)

            if image_type not in valid_image_types:
                return CustomResponseHandler.error(
                    message="File type not allowed. Only images are accepted.",
                    status_code=HTTPStatus.BAD_REQUEST
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

            return CustomResponseHandler.success(
                message="User profile image updated successfully",
                data={"file_location": file_location},
                status_code=HTTPStatus.OK
            )

        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
