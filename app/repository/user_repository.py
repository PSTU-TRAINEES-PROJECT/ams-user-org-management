from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import Status
from schemas.base import User, UserUpdateData
from sqlalchemy.future import select

class UserRepository:
    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        query = select(User).where(User.email == email, User.deleted_at == None)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_user_by_user_id(self, user_id: int, db: AsyncSession) -> User:
        query = select(User).where(User.id == user_id)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_all_users(self, db: AsyncSession) -> list[User]:
        query = select(User)
        result = await db.execute(query)
        users = result.scalars().all()
        return users

    async def update_user_status(self, user: User, status: Status, db: AsyncSession):
        user.status = status
        await db.commit()
        await db.refresh(user)


    async def update_user(self, user_id: int, user_update_data: UserUpdateData, db: AsyncSession):
        user = await self.get_user_by_user_id(user_id, db)
        if user:
            if user_update_data.first_name is not None:
                user.first_name = user_update_data.first_name
            if user_update_data.last_name is not None:
                user.last_name = user_update_data.last_name
            if user_update_data.mobile is not None:
                user.mobile = user_update_data.mobile
            if user_update_data.age is not None:
                user.age = user_update_data.age
            if user_update_data.email is not None:
                user.email = user_update_data.email
            if user_update_data.password is not None:
                user.password_hash = user_update_data.password
            await db.commit()
            await db.refresh(user)

    async def delete_user(self, user_id: int, db: AsyncSession):
        user = await self.get_user_by_user_id(user_id, db)
        await db.delete(user)
        await db.commit()

    async def update_user_profile_image(self, user: User, image_path: str, db: AsyncSession):
        user.profile_image = image_path
        await db.commit()
        await db.refresh(user)
