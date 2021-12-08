import os

APP_NAME = os.getenv('APP_NAME')

AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

AZURE_STORAGE_CONTAINERS = {
    'DOCUMENTS': 'documents',
    'DOCUMENT_PARAGRAPHS': 'documentparagraphs',
    'ANNOTATED_PARAGRAPHS': 'annotatedparagraphs',
    'DOCUMENT_FIELDS': 'documentfields',
    'CUSTOM_FIELDS_MODELS': 'customfieldsmodels'
}

CORE_APP_URL = os.getenv('CORE_APP_URL')
CORE_CHANGE_PROCESS_STATUS = "/api/v1/document-processing-result-update"
CORE_DOCUMENT_TYPE_CONFIG = "/api/v1/document-type/{document_type_id}/config"

CORE_CHANGE_PROCESS_STATUS_URL = CORE_APP_URL + CORE_CHANGE_PROCESS_STATUS
CORE_DOCUMENT_TYPE_CONFIG_URL = CORE_APP_URL + CORE_DOCUMENT_TYPE_CONFIG

ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')