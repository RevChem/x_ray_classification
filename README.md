Этот репозиторий представляет собой пример (шаблон) архитектуры для систем машинного обучения в медицине, построенной на асинхронной обработке изображений.

Проект изначально реализует простую классификацию рентгенограмм на "пневмония" / "здоровый" , но главная цель — продемонстрировать масштабируемую и расширяемую инфраструктуру , которую можно адаптировать под различные задачи.

### Переменные окружения

Для запуска проекта создайте файл `.env` в корне проекта со следующими переменными:

```
DB_HOST=localhost     # Адрес сервера БД (localhost, если локально)
DB_PORT=5432          # Порт PostgreSQL (по умолчанию 5432)
DB_NAME=primer_3      # Название базы данных
DB_USER=postgres      # Пользователь БД
DB_PASSWORD=          # Пароль пользователя для postgres

# Настройки Redis
REDIS_HOST=localhost  # Адрес Redis-сервера
REDIS_PORT=6379       # Порт Redis (по умолчанию 6379)
REDIS_PASSWORD=       # Пароль для Redis (по умолчанию пуст)    
```

### Упрощённая структура проекта

```
x-ray-classification/
├── app/
│   ├── main.py                   # Точка входа приложения (FastAPI)
│   ├── config.py                 # Настройки (конфигурация)
│   ├── database.py               # Подключение к PostgreSQL через SQLAlchemy
│   │
│   ├── api/
│   │   ├── router.py             # Главный роутер API
│   │   └── predict.py            # Эндпоинт для предсказания
│   │
│   ├── tasks/
│   │   ├── celery_app.py         # Настройка Celery
│   │   └── config.py             # Конфигурация задач
│   │
│   ├── models/                   # PyTorch модели
│   │   └── resnet50_pneumonia.pth  # Веса модели (в .gitignore)
│   │
│   ├── diagnosis/                # Модуль для задачи диагностики
│   │   ├── models.py             # ORM-модели (SQLAlchemy)
│   │   ├── schemas.py            # Pydantic-схемы
│   │   ├── dao.py                # Data Access Object (работа с БД)
│   │   ├── router.py             # Роуты для диагностики
│   │   └── rb.py                 # Role-based логика (опционально)
│   │
│   ├── users/                    # Модуль пользователей (если нужно)
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── dao.py
│   │   └── router.py
│   │
│   └── monitoring/               # Метрики, логирование
│       ├── middleware.py
│       └── metrics.py
│
├── alembic.ini                   # Конфиг Alembic
├── alembic/                      # Миграции БД
│   ├── env.py
│   ├── script.py.mako
│   └── versions/                 # Автогенерируемые миграции
│       └── *.py
│
├── requirements.txt              # Зависимости
├── .env                          # Переменные окружения (в .gitignore)
├── .gitignore
│
├── uploads/                      # Загруженные изображения (в .gitignore)
├── test_images/                  # Примеры изображений для теста
│   ├── normal.jpeg
│   └── pneumonia.jpeg
│
└── README.md
```
