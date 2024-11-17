from pydantic import BaseModel

from utils.helpers.enums import PlatformTypes


class ServiceProfileCreateData(BaseModel):
    platform_type: PlatformTypes
    department: str
    upload_document: list[dict]
    name_of_degree: str
    current_working_institution: str
    years_of_experience: int

    class Config:
        schema_extra = {
            "example": {
                "platform_type": 1,
                "department": "Cardiology",
                "upload_document": [
                    {
                        "file_base64": "base64_encoded_string" , 
                        "file_name": "file_name.pdf"
                    },
                    {
                        "file_base64": "base64_encoded_string" , 
                        "file_name": "file_name.png"
                    }
                ],
                "name_of_degree": "Doctor of Medicine (MD)",
                "current_working_institution": "City General Hospital",
                "years_of_experience": 5
            }
        }

