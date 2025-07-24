from fastapi import APIRouter, Depends
from app.diagnosiss.dao import DiagnosisDao
from app.diagnosiss.schemas import SDiagnosis
from typing import Optional 
from app.diagnosiss.rb import RBDiagnosis
from app.diagnosiss.sql_enums import DiagnosisEnum


router = APIRouter(prefix = '/diagnosiss', tags = ['Работа с таблицей диагнозов'])

@router.get("/{id}", summary="Получить карточку пользователя по ID")
async def find_one_or_none_by_id(request_body: RBDiagnosis = Depends()) -> Optional[SDiagnosis]:
    return await DiagnosisDao.find_one_or_none_by_id(**request_body.to_dict())


@router.get("/", summary="Получить всех пользователей")
async def find_all() -> list[SDiagnosis]:
    return await DiagnosisDao.find_all()


@router.post("/add/")
async def add_user(user: SDiagnosis) -> dict:
    user = await DiagnosisDao.add(**user.dict())
    if user:
        return {"message": "Пользователь успешно добавлен!", "user": user}
    else:
        return {"message": "Ошибка при добавлении пользователя!"}


# @router.delete("/dell/{id}")
# async def delete(id: int) -> dict:
#     check = await UserDAO.delete(id=id)
#     if check:
#         return {"message": f"Студент с ID {id} удален!"}
#     else:
#         return {"message": "Ошибка при удалении студента!"}