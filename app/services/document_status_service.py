import requests

from app.services.encryption_service import EncryptionService
from app.config.common import (APP_NAME, CORE_CHANGE_TRAINING_STATUS_URL,
                               CORE_TRAINING_STATUS_FINISHED_URL, CORE_TRAINING_STATUS_FAILED_URL)


# TODO change name
def update_training_information_finished(trained_model_id, model_location):
    data = {'trained_model_id': trained_model_id, 'model_location': model_location}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}

    requests.post(CORE_TRAINING_STATUS_FINISHED_URL, data=data, headers=headers)


def update_training_information_failed(trained_model_id):
    data = {'trained_model_id': trained_model_id}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}

    requests.post(CORE_TRAINING_STATUS_FAILED_URL, data=data, headers=headers)


def change_training_status(trained_model_id, model_name, status):
    data = {"trained_model_id": trained_model_id,
            "model_location": model_name,
            "status": status.value}
    headers = {'authorization': EncryptionService.encrypt(APP_NAME)}
    requests.post(url=CORE_CHANGE_TRAINING_STATUS_URL,
                  data=data,
                  headers=headers)
