import os
import ssl
from celery import Celery
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_PORT: int
    REDIS_PASSWORD: str
    BASE_URL: str
    REDIS_HOST: str
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()
redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
ssl_options = {"ssl_cert_reqs": ssl.CERT_NONE}
celery_app = Celery("celery_worker", broker=redis_url, backend=redis_url)