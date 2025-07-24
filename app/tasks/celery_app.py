from celery import Celery
from app.tasks.config import redis_url
from PIL import Image
import io
from loguru import logger
from ..api.predict import XRayClassifier


celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)


celery_app.conf.update(
    task_serializer='json',   
    result_serializer='json',   
    accept_content=['json'],    
    enable_utc=True,  
    timezone='Europe/Moscow', 
    broker_connection_retry_on_startup=True,   
    task_acks_late=True,     
    task_reject_on_worker_lost=True, 
)

MODEL_PATH = "weights/resnet50_pneumonia.pth"
model = XRayClassifier(MODEL_PATH)

@celery_app.task(
    name='classify_xray_task',   
    bind=True,   
    max_retries=3,   
    default_retry_delay=5  
)
def classify_xray_task(self, image_bytes: bytes):
    """Задача для классификации рентгенограммы"""
    try:
        logger.info(f"Начало обработки задачи {self.request.id}")
        Image.open(io.BytesIO(image_bytes)).verify()
        result = model.predict(image_bytes)
        logger.info(f"Задача {self.request.id} успешно завершена")
        return {"result": result}
    except Exception as exc:
        logger.error(f"Classification error: {exc}", exc_info=True)
        self.retry(exc=exc)