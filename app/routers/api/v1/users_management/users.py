from fastapi import APIRouter, Depends
from repository.department_repository import DepartmentRepository
from repository.service_profile_repository import ServiceProfileRepository
from repository.user_document_repository import UserDocumentRepository
from schemas.base import UserUpdateData
from core.middleware import authenticate_header
from utils.helpers.enums import Status
from repository.database import get_db
from repository.user_repository import UserRepository
from services.users import UserService
from sqlalchemy.ext.asyncio import  AsyncSession
from fastapi import File, UploadFile

user_router = APIRouter()
repository = UserRepository()
service_profile_repository = ServiceProfileRepository()
user_document_repository = UserDocumentRepository()
department_repository = DepartmentRepository()
user_service = UserService(repository, service_profile_repository, user_document_repository, department_repository)


@user_router.get("/all-users")
async def get_users(db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.get_all_users(db)



@user_router.post("/update-user-status")
async def update_user_status(status: Status, db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.update_user_status(x_user_id_from_request, status, db)



@user_router.get("/get-user")
async def get_user(db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.get_user(x_user_id_from_request, db)


@user_router.post("/update-user")
async def update_user(user_update_data: UserUpdateData, db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.update_user(x_user_id_from_request, user_update_data, db)



@user_router.delete("/delete-user")
async def delete_user(db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.delete_user(x_user_id_from_request, db)

@user_router.post("/update-user-profile-image")
async def update_user_profile_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.update_user_profile_image(x_user_id_from_request, file, db)