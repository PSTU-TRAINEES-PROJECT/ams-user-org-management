from schemas.base import Base
from schemas.users import current_time
from sqlalchemy import Column, DateTime, Integer, String, ARRAY


class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    years_of_experience = Column(Integer, nullable=False)
    current_working_institution = Column(String(100), nullable=False)
    name_of_degree = Column(String(100), nullable=False)
    
    department_id = Column(Integer, nullable=False)
    document_id_list = Column(ARRAY(Integer), nullable=False)

    created_at = Column(DateTime(timezone=True), default=current_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=current_time, nullable=False, onupdate=current_time)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "years_of_experience": self.years_of_experience,
            "current_working_institution": self.current_working_institution,
            "name_of_degree": self.name_of_degree,
            "department_id": self.department_id,
            "document_id_list": self.document_id_list,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
        }
