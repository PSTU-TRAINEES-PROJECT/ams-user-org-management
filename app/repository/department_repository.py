from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import PlatformTypes
from schemas.base import Department
from sqlalchemy.future import select

class DepartmentRepository:
    async def get_department_id_by_name_and_platform_type(self, department_name: str, platform_type: PlatformTypes, db: AsyncSession) -> Department:
        query = select(Department).where(Department.name == department_name, Department.platform_type == platform_type)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_department_by_id_and_platform_type(self, department_id: int, platform_type: int, db: AsyncSession) -> Department:
        query = select(Department).where(Department.id == department_id, Department.platform_type == platform_type)
        result = await db.execute(query)
        return result.scalars().first()


    async def create_department(self, department_name: str, platform_type: PlatformTypes, db: AsyncSession) -> Department:
        new_department = Department(name=department_name, platform_type=platform_type)
        db.add(new_department)
        await db.commit()
        return new_department
