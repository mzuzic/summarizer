import os

from flask import Flask
from config import config, Config
from celery import Celery


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
celery.autodiscover_tasks(['app.tasks'])


def create_app():
    app = Flask(os.getenv('APP_NAME'))
    app.config.from_object(config)

    celery.conf.update(app.config)

    return app
