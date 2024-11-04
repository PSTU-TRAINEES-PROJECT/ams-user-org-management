from fastapi import APIRouter, Depends
from repository.department_repository import DepartmentRepository
from schemas.base import UserUpdateData, ServiceProfileCreateData
from core.middleware import authenticate_header
from utils.helpers.enums import Status
from repository.database import get_db
from repository.service_profile_repository import ServiceProfileRepository
from repository.user_document_repository import UserDocumentRepository
from services.service_profile import ServiceProfileService
from sqlalchemy.ext.asyncio import  AsyncSession

service_profile_router = APIRouter()

service_profile_repository = ServiceProfileRepository()
user_document_repository = UserDocumentRepository()
department_repository = DepartmentRepository()

service_profile_service = ServiceProfileService(service_profile_repository, department_repository, user_document_repository)



@service_profile_router.post("/create-service-profile")
async def create_service_profile(profile_data: ServiceProfileCreateData, db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await service_profile_service.create_service_profile(int(x_user_id_from_request), profile_data, db)



@service_profile_router.get("/get-service-profile")
async def get_self_service_profile(db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await service_profile_service.get_self_service_profile(int(x_user_id_from_request), db)





