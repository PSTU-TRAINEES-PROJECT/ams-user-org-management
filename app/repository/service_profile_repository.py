from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import PlatformTypes, Status
from schemas.base import User, ServiceProfileCreateData, Doctor, Engineer, Teacher, PublicFigure, Business, Lawyer
from sqlalchemy.future import select

class ServiceProfileRepository:
    async def get_service_profile_by_user_id_platform_type(self, user_id: str, platform_type: PlatformTypes, db: AsyncSession):
        if platform_type == PlatformTypes.DOCTOR:
            query = select(Doctor).where(
                Doctor.user_id == user_id,
                Doctor.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        elif platform_type == PlatformTypes.ENGINEER:
            query = select(Engineer).where(
                Engineer.user_id == user_id,
                Engineer.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        elif platform_type == PlatformTypes.TEACHER:
            query = select(Teacher).where(
                Teacher.user_id == user_id,
                Teacher.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        elif platform_type == PlatformTypes.PUBLIC_FIGURE:
            query = select(PublicFigure).where(
                PublicFigure.user_id == user_id,
                PublicFigure.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        elif platform_type == PlatformTypes.BUSINESS:
            query = select(Business).where(
                Business.user_id == user_id,
                Business.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        elif platform_type == PlatformTypes.LAWYER:
            query = select(Lawyer).where(
                Lawyer.user_id == user_id,
                Lawyer.deleted_at == None
            )
            result = await db.execute(query)
            return result.scalars().first()
            
        return None
    
    
    async def get_service_profile_by_user_id(self, user_id: str, db: AsyncSession):
        query = select(Doctor).where(
            Doctor.user_id == user_id,
            Doctor.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.DOCTOR.value
        
        query = select(Engineer).where(
            Engineer.user_id == user_id,
            Engineer.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.ENGINEER.value
        
        query = select(Teacher).where(
            Teacher.user_id == user_id,
            Teacher.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.TEACHER.value
        
        query = select(PublicFigure).where(
            PublicFigure.user_id == user_id,
            PublicFigure.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.PUBLIC_FIGURE.value
        
        query = select(Business).where(
            Business.user_id == user_id,
            Business.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.BUSINESS.value
        
        query = select(Lawyer).where(
            Lawyer.user_id == user_id,
            Lawyer.deleted_at == None
        )
        result = await db.execute(query)
        profile = result.scalars().first()
        if profile:
            return profile , PlatformTypes.LAWYER.value
        
        return None , None
    
    
    async def create_service_profile(self, user_id: int, profile_data: ServiceProfileCreateData, department_id: int, document_ids: list[int], db: AsyncSession):
        if profile_data.platform_type == PlatformTypes.DOCTOR:
            new_service_profile = Doctor(
                user_id=user_id,
                name_of_degree=profile_data.name_of_degree, 
                current_working_institution=profile_data.current_working_institution, 
                years_of_experience=profile_data.years_of_experience,
                department_id=department_id,
                document_id_list=document_ids
            )
            db.add(new_service_profile)
            await db.commit()
            return new_service_profile

