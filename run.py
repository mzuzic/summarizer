
from init_files_handler import download_datasets, download_model

download_datasets()
download_model()

import os
from app import create_app
from app.api import index
from waitress import serve

app = create_app()
app.register_blueprint(index)


if __name__ == '__main__':
    host = os.environ.get('IP', '0.0.0.0')
    port = int(os.environ.get("PORT", 5006))

    serve(app, host=host, port=port) if (os.getenv('APP_ENV') == 'prod') else app.run(host=host, port=port)