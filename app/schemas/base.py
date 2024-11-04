from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


from schemas.language import Language
from schemas.users import User, UserUpdateData
from schemas.organization import Organization
from schemas.membership import Membership
from schemas.service_profile import ServiceProfileCreateData
from schemas.department import Department
from schemas.doctor import Doctor
from schemas.business import Business
from schemas.engineer import Engineer
from schemas.lawyer import Lawyer
from schemas.public_figure import PublicFigure
from schemas.teacher import Teacher
from schemas.user_document import UserDocument

