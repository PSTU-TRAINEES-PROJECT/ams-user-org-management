from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from repository.organization_repository import OrganizationRepository
from repository.membership_repository import MembershipRepository
from utils.helpers.response_handler import CustomResponseHandler



class OrganizationService:
    def __init__(self, organization_repository: OrganizationRepository, membership_repository: MembershipRepository):
        self.organization_repository = organization_repository
        self.membership_repository = membership_repository

    async def create_organization(self, user_id: int, name: str, db: AsyncSession):
        try:
            existing_organization = await self.organization_repository.get_organization_by_name(name, db)
            if existing_organization:
                return CustomResponseHandler.error(
                    message="Organization with this name already exists.",
                    status_code=HTTPStatus.CONFLICT
                )

            user_membership = await self.membership_repository.get_membership_by_user_id_and_role(user_id, 'admin', db)
            if user_membership:
                return CustomResponseHandler.error(
                    message="User already has an organization with admin role.",
                    status_code=HTTPStatus.CONFLICT
                )
            

            new_organization = await self.organization_repository.create_organization(name, db)
            

            new_membership = await self.membership_repository.create_membership(user_id, new_organization.id, 'admin', db)

            return CustomResponseHandler.success(
                message="Organization created successfully",
                data={"organization_name": new_organization.name},
                status_code=HTTPStatus.CREATED
            )
        except Exception as e:
            return CustomResponseHandler.error(
                message=f"Internal server error. ERROR: {e}",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR
            )
