from app.dao.base import BaseDao
from app.diagnosiss.models import Diagnosis


class DiagnosisDao(BaseDao):
    model = Diagnosis