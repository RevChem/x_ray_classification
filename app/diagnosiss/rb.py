from app.diagnosiss.sql_enums import DiagnosisEnum


class RBDiagnosis:
    def __init__(
        self,
        diagnosis_id: int | None = None,
        user_id: int | None = None,
        image_path: str | None = None,
        diagnosis: DiagnosisEnum | None = None,
    ):
        self.id = diagnosis_id
        self.user_id = user_id
        self.image_path = image_path
        self.diagnosis = diagnosis

    def to_dict(self) -> dict:
        return {
            key: value for key, value in {
                "id": self.id,
                "user_id": self.user_id,
                "image_path": self.image_path,
                "diagnosis": self.diagnosis
            }.items() if value is not None
        }