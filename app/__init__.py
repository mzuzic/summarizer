import os

from flask import Flask
from config import config


def create_app():
    app = Flask(os.getenv('APP_NAME'))
    app.config.from_object(config)

    return app
