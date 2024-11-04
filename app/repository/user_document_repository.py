from sqlalchemy.ext.asyncio import AsyncSession
from schemas.base import Organization, UserDocument
from sqlalchemy.future import select

class UserDocumentRepository:

    async def create_user_document(self, filename: str, db: AsyncSession) -> UserDocument:
        new_document = UserDocument(file_name=filename)
        db.add(new_document)
        await db.commit()
        await db.refresh(new_document)
        return new_document

    async def get_user_documents_by_ids(self, document_id_list: list[int], db: AsyncSession) -> list[UserDocument]:
        query = select(UserDocument).where(UserDocument.id.in_(document_id_list))
        result = await db.execute(query)
        return result.scalars().all()
