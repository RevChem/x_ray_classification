import io
import os
from PIL import Image
from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends
from app.tasks.celery_app import classify_xray_task
from app.diagnosiss.models import Diagnosis
from app.database import get_db
from fastapi.concurrency import run_in_threadpool
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.diagnosiss.sql_enums import DiagnosisEnum


router = APIRouter(prefix='/predict', tags=['Получение предсказания'])

@router.post("/")
async def predict_pneumonia(
    file: UploadFile = File(...),
    user_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Эндпоинт с немедленной записью диагноза"""
    try:
        image_bytes = await file.read()
        Image.open(io.BytesIO(image_bytes)).verify()
        
        task = classify_xray_task.delay(image_bytes)
        result = task.get(timeout=5) 
        
        image_path = f"uploads/{task.id}.jpg"
        os.makedirs('uploads', exist_ok=True)
        await run_in_threadpool(lambda: Path(image_path).write_bytes(image_bytes))
        
        diagnosis = Diagnosis(
            user_id=user_id,
            image_path=image_path,
            diagnosis=DiagnosisEnum[result['result'].upper()] 
        )
        db.add(diagnosis)
        await db.commit()
        
        return {
            "task_id": task.id,
            "diagnosis": diagnosis.diagnosis.value,
            "status": "completed"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))