import os

BROKER_URL = os.getenv('RABBITMQ_BROKER_URL')
BROKER_HEARTBEAT = 0
CELERY_RESULT_BACKEND = 'Events.extended.ExtendedMongoBackend'
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": os.getenv('MONGO_HOST'),
    "port": 27017,
    "database": "admin",
    "taskmeta_collection": "event_async",
    "user": os.getenv('MONGO_USERNAME'),
    "password": os.getenv('MONGO_PASSWORD')
}
