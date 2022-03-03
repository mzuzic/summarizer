import os

APP_NAME = os.getenv('APP_NAME')
DEV_ENV = os.getenv('APP_ENV', 'dev') == 'dev'

database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')

DATABASE_CONNECTION_URI = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
