from fastapi import APIRouter, Depends
from core.middleware import authenticate_header
from utils.helpers.enums import Status
from repository.database import get_db
from repository.user_repository import UserRepository
from services.users import UserService
from sqlalchemy.ext.asyncio import  AsyncSession

user_router = APIRouter()
repository = UserRepository()
user_service = UserService(repository)


@user_router.get("/all-users")
async def get_users(db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.get_all_users(db)



@user_router.post("/update-user-status/{user_id}")
async def update_user_status(user_id: int, status: Status, db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await user_service.update_user_status(user_id, status, db)


