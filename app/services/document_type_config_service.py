import requests

from app.services.encryption_service import EncryptionService
from app.config.common import APP_NAME, CORE_DOCUMENT_TYPE_CONFIG_URL


def get_document_type_config(document_type_id):
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}
    requests.get(CORE_DOCUMENT_TYPE_CONFIG_URL.format(document_type_id=document_type_id), headers=headers)
