from schemas.base import Base
from schemas.users import current_time
from sqlalchemy import Column, DateTime, Integer, String


class UserDocument(Base):
    __tablename__ = "user_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(200), unique=True, nullable=False)
    # object_key = Column(String(100), nullable=False)
    # owner_type = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_time, nullable=False, onupdate=current_time)
    deleted_at = Column(DateTime(timezone=True), nullable=True)