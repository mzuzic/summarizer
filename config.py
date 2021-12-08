import os
from flask import config

if os.getenv('APP_ENV', 'dev') == 'dev':
    from dotenv import load_dotenv
    load_dotenv()

class BaseConfig:
    CACHE_TYPE = os.environ.get('CACHE_TYPE')
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL')
    SECRET_KEY = os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else None


config = BaseConfig
