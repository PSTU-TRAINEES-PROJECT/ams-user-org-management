from sqlalchemy.ext.asyncio import AsyncSession
from utils.helpers.enums import Status
from schemas.base import User
from sqlalchemy.future import select

class UserRepository:
    async def get_user_by_email(self, email: str, db: AsyncSession) -> User:
        query = select(User).where(User.email == email, User.deleted_at == None)
        result = await db.execute(query)
        user = result.scalars().first()
        return user
    
    async def get_user_by_username(self, username: str, db: AsyncSession) -> User:
        query = select(User).where(User.username == username)
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



