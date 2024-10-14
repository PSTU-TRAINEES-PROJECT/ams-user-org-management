from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.middleware import authenticate_header
from services.organization_service import OrganizationService
from repository.database import get_db
from repository.organization_repository import OrganizationRepository
from repository.membership_repository import MembershipRepository


organization_router = APIRouter()
organization_repository = OrganizationRepository()
membership_repository = MembershipRepository()
organization_service = OrganizationService(organization_repository, membership_repository)


@organization_router.post("/create-organization")
async def create_organization(name: str, user_id: int, db: AsyncSession = Depends(get_db), x_user_id_from_request: str = Depends(authenticate_header)):
    print(f"x_user_id_from_request: {x_user_id_from_request}")
    return await organization_service.create_organization(user_id, name, db)

