import uuid
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.diagnosiss.sql_enums import DiagnosisEnum
#from app.users.models import User

class Diagnosis(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    image_path: Mapped[str] = mapped_column(String, nullable=False)
    diagnosis: Mapped[DiagnosisEnum] = mapped_column(
        default = DiagnosisEnum.NORMAL)
    
    user: Mapped["User"] = relationship(back_populates="diagnosis")
    extend_existing = True

    def __repr__(self):
        return str(self.__dict__)
