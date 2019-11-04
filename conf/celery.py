import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv("%s%s" % (BASE_DIR, Path("/.env")), override=True)

BROKER_URL = os.getenv('RABBITMQ_BROKER_URL')
