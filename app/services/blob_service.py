import os
from azure.storage.blob import BlobServiceClient


class BlobService:
    """
    Defines methods for Azure Blob Storage access.
    """
    def __init__(self):
        self.service = None
        self.connection_string = None

    def set_sas(self, connection_string):
        self.connection_string = connection_string
        self.service = BlobServiceClient.from_connection_string(connection_string)

    def upload(self, file_path, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(container=shared_storage_container, blob=blob_name)

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data)

    def download(self, local_path, shared_storage_container, blob_name):
        blob_client = self.service.get_blob_client(container=shared_storage_container, blob=blob_name)

        with open(local_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

    @staticmethod
    def create_anonymous():
        blob_service = BlobService()
        blob_service.set_sas(os.environ.get('AZURE_STORAGE_CONNECTION_STRING'))
        return blob_service
