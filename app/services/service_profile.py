from fastapi.responses import JSONResponse
from http import HTTPStatus
from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import PlatformTypes
from utils.helpers.file_handler import get_base64_file, save_base64_file
from repository.service_profile_repository import ServiceProfileRepository
from repository.department_repository import DepartmentRepository
from repository.user_document_repository import UserDocumentRepository
from schemas.base import ServiceProfileCreateData

class ServiceProfileService:
    def __init__(self, service_profile_repository: ServiceProfileRepository, department_repository: DepartmentRepository, user_document_repository: UserDocumentRepository):
        self.service_profile_repository = service_profile_repository
        self.department_repository = department_repository
        self.user_document_repository = user_document_repository


    async def create_service_profile(self, x_user_id_from_request: int, profile_data: ServiceProfileCreateData, db: AsyncSession):
        try:
            existing_service_profile = await self.service_profile_repository.get_service_profile_by_user_id_platform_type(x_user_id_from_request, profile_data.platform_type, db)
            if existing_service_profile:
                return JSONResponse(
                    status_code=HTTPStatus.CONFLICT,
                    content={"message": "Service profile already exists for this user."}
                )
            
            department = await self.department_repository.get_department_id_by_name_and_platform_type(profile_data.department, profile_data.platform_type, db)
            if not department:
                department = await self.department_repository.create_department(profile_data.department, profile_data.platform_type, db)
            
            document_ids = []
            for base64_doc in profile_data.upload_document:
                try:
                    filename = save_base64_file(base64_doc.get("file_base64"), base64_doc.get("file_name"))
                    document = await self.user_document_repository.create_user_document(filename, db)
                    document_ids.append(document.id)
                    
                except Exception as e:
                    return JSONResponse(
                        status_code=HTTPStatus.BAD_REQUEST,
                        content={"message": f"Error processing document: {str(e)}"}
                    )
            
            new_service_profile = await self.service_profile_repository.create_service_profile(x_user_id_from_request, profile_data, department.id, document_ids, db)
            

            return JSONResponse(
                status_code=HTTPStatus.CREATED,
                content={"message": "Service profile created successfully"}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )
    
    
    async def get_self_service_profile(self, x_user_id_from_request: int, db: AsyncSession):
        try:
            existing_service_profile, platform_type = await self.service_profile_repository.get_service_profile_by_user_id(x_user_id_from_request, db)
            if not existing_service_profile:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": "Service profile not found"}
                )
            
            document_list = await self.user_document_repository.get_user_documents_by_ids(existing_service_profile.document_id_list, db)
            formatted_documents = [
                get_base64_file(doc.file_name) for doc in document_list
            ]
            
            department = await self.department_repository.get_department_by_id_and_platform_type(existing_service_profile.department_id, platform_type, db)
            
            service_profile_dict = existing_service_profile.to_dict()
            service_profile_dict.pop('document_id_list', None)
            service_profile_dict['department_name'] = department.name
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={"message": "Service profile fetched successfully", "data": {"service_profile": service_profile_dict, "document_list": formatted_documents}}
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )


    async def get_list_service_profiles(self, platform_type: int, db: AsyncSession):
        try:
            try:
                platform_enum = PlatformTypes(platform_type)
            except ValueError:
                return JSONResponse(
                    status_code=HTTPStatus.BAD_REQUEST,
                    content={"message": "Invalid platform type"}
                )
                
            # Get all profiles for the specified platform type
            profile_list = await self.service_profile_repository.get_all_profiles_by_platform_type(platform_enum, db)
            if not profile_list:
                return JSONResponse(
                    status_code=HTTPStatus.NOT_FOUND,
                    content={"message": f"No {platform_enum.name.lower()}s found"}
                )
            
            formatted_profiles = []
            for profile in profile_list:
                # Get documents for each profile
                document_list = await self.user_document_repository.get_user_documents_by_ids(profile.document_id_list, db)
                formatted_documents = [
                    get_base64_file(doc.file_name) for doc in document_list
                ]
                
                # Get department info
                department = await self.department_repository.get_department_by_id_and_platform_type(
                    profile.department_id, 
                    platform_enum.value, 
                    db
                )
                
                # Format profile data
                profile_dict = profile.to_dict()
                profile_dict.pop('document_id_list', None)
                profile_dict['department_name'] = department.name if department else None
                profile_dict['documents'] = formatted_documents
                
                formatted_profiles.append(profile_dict)

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": f"{platform_enum.name.lower()} list fetched successfully", 
                    "data": formatted_profiles
                }
            )
        except Exception as e:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={"message": f"Internal server error. ERROR: {e}"}
            )

