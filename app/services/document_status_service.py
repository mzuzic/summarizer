import requests

from app.services.encryption_service import EncryptionService
from app.config.common import APP_NAME, CORE_CHANGE_PROCESS_STATUS_URL, CORE_TRAINING_STATUS_FINISHED_URL, CORE_TRAINING_STATUS_FAILED_URL


def change_process_status(id, file_name: str, process_type: str, process_result: str) -> None:
    post_data = {'document_id': id, 'file_name': file_name, "process_type": process_type, "process_result": process_result}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}
    requests.post(CORE_CHANGE_PROCESS_STATUS_URL, data=post_data, headers=headers)


# TODO change name
def update_training_information_finished(trained_model_id, model_location):
    data = {'trained_model_id': trained_model_id, 'model_location': model_location}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}

    requests.post(CORE_TRAINING_STATUS_FINISHED_URL, data=data, headers=headers)


def update_training_information_failed(trained_model_id):
    data = {'trained_model_id': trained_model_id}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}

    requests.post(CORE_TRAINING_STATUS_FAILED_URL, data=data, headers=headers)
