from pydantic import BaseModel, Field
from typing import Optional
from app.diagnosiss.sql_enums import DiagnosisEnum

class SDiagnosis(BaseModel):
    diagnosis: Optional[DiagnosisEnum]
    user_id: Optional[int] = Field(None, description="id пользователя")
    image_path: Optional[str] = Field(None, description="Путь к рентгенограмме")

