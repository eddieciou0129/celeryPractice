import os
from kombu import Exchange, Queue

BROKER_URL = os.getenv('RABBITMQ_BROKER_URL')
BROKER_HEARTBEAT = 0
CELERY_RESULT_BACKEND = 'Events.extended.ExtendedMongoBackend'
CELERY_INCLUDE = ['Events.TestEvent', 'Events.TestEventTWO']
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": os.getenv('MONGO_HOST'),
    "port": 27017,
    "database": "admin",
    "taskmeta_collection": "event_async",
    "user": os.getenv('MONGO_USERNAME'),
    "password": os.getenv('MONGO_PASSWORD')
}

CELERY_QUEUES = (
    Queue('celery', Exchange('celery'), routing_key='celery', consumer_arguments={'x-priority': 9}),
    Queue('common', Exchange('common'), routing_key='common', consumer_arguments={'x-priority': 5}),
    Queue('payment', Exchange('payment'), routing_key='payment.#', consumer_arguments={'x-priority': 2}),
    Queue('transfer', Exchange('transfer'), routing_key='transfer.#', consumer_arguments={'x-priority': 1})
)

CELERY_ROUTES = {
    'celery': {'queue': 'celery', 'routing_key': 'celery'},
    'common': {'queue': 'common', 'routing_key': 'common'},
    'payment.*': {'queue': 'payment', 'routing_key': 'payment.#'},
    'transfer.*': {'queue': 'transfer', 'routing_key': 'transfer.#'}
}