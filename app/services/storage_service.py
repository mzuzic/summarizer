import os
import pickle
import localstack_client.session as boto3

from congablobservice import BlobService
from app.config.common import AZURE_STORAGE_CONTAINERS, AZURE_STORAGE_CONNECTION_STRING
from app.constants import ERROR_BLOB_DOESNT_EXIST

from .file_service import TemporaryFile


class StorageServiceConfig:
    def __init__(self, shared_storage_container_custom_fields_models):
        self.shared_storage_container_custom_fields_models = shared_storage_container_custom_fields_models

    @staticmethod
    def default():
        return StorageServiceConfig(AZURE_STORAGE_CONTAINERS.get('CUSTOM_FIELDS_MODELS'))


class StorageService:
    def __init__(self, storage_config=StorageServiceConfig.default()):
        self.blob_service = BlobService.create_anonymous(azure_storage_connection_string=AZURE_STORAGE_CONNECTION_STRING)
        self.config = storage_config

    def upload(self, temp_file_path):
        self.blob_service.upload(temp_file_path, self.config.shared_storage_container_custom_fields_models,
                                 os.path.basename(temp_file_path))

    def upload_ml_model(self, model_name, model):
        with open(f'{model_name}.pkl', 'wb') as f:
            pickle.dump(model, f)

        self.upload(f'{model_name}.pkl')
        os.remove(f'{model_name}.pkl')

        return model_name

    def download(self, tempfile, blob_name):
        print(f"Downloading {blob_name}", flush=True)

        blob = self.blob_service.get_specific_blob_client(conn_str=AZURE_STORAGE_CONNECTION_STRING,
                                                          container_name=self.config.shared_storage_container_custom_fields_models,
                                                          blob_name=blob_name)
        if not blob.exists():
            raise ValueError(ERROR_BLOB_DOESNT_EXIST)

        with open(tempfile.file_path, "wb") as download_file:
            download_file.write(blob.download_blob().readall())

        return tempfile

    def download_ml_model(self, model_location):
        tempfile = TemporaryFile('test', '.pkl')
        tempfile = self.download(tempfile, model_location)
        with open(tempfile.file_path, 'rb') as f:
            model = pickle.load(f)
        return model

    def does_blob_exist(self, blob_name):
        return self.blob_service.check_does_blob_exist(conn_str=AZURE_STORAGE_CONNECTION_STRING,
                                                       blob_name=blob_name,
                                                       container_name=self.config.shared_storage_container_custom_fields_models)


class S3StorageService:
    def __init__(self, storage_config=StorageServiceConfig.default()):
        # self.blob_service = boto3.client('s3', endpoint_url='http://localstack-container:4572')
        session = boto3.Session(localstack_host="localstack-container")
        self.blob_service = session.client('s3')
        self.config = storage_config

    def store_in_temp_file(self, temp_file, document_file):
        os.write(temp_file, document_file.read())

    def upload(self, temp_file_path):
        print(f"Uploading {temp_file_path} to S3", flush=True)

        self.blob_service.upload_file(temp_file_path,
                                      self.config.shared_storage_container_document_fields,
                                      os.path.basename(temp_file_path))

    def upload_ml_model(self, model_name, model):
        with open(f'{model_name}.pkl', 'wb') as f:
            pickle.dump(model, f)

        self.upload(f'{model_name}.pkl')
        os.remove(f'{model_name}.pkl')

        return model_name

    def delete_blob(self, blob_name):
        self.blob_service.Object(self.config.shared_storage_container_document_paragraphs, blob_name).delete()

    def download(self, tempfile, blob_name):
        print(f"Downloading {blob_name} from S3", flush=True)

        if not self.does_blob_exist(blob_name):
            raise ValueError(ERROR_BLOB_DOESNT_EXIST)

        with open(tempfile.file_path, 'wb') as data:
            self.blob_service.download_fileobj(self.config.shared_storage_container_custom_fields_models, blob_name, data)

        return tempfile

    def download_ml_model(self, model_location):
        tempfile = TemporaryFile('test', '.pkl')
        tempfile = self.download(tempfile, model_location)
        with open(tempfile.file_path, 'rb') as f:
            model = pickle.load(f)
        return model

    def does_blob_exist(self, blob_name, container_name):
        return self.blob_service.head_object(Bucket=self.config.shared_storage_container_custom_fields_models, Key=blob_name)


storage_service = S3StorageService()
