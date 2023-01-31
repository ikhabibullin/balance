import os

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_BACKEND_URL = os.getenv('CELERY_BACKEND_URL', 'redis://localhost:6379')

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'balance')
DB_USER = os.getenv('DB_USER', 'balance')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'balance')
DB_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
