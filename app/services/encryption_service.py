from cryptography.fernet import Fernet

from app.config.common import ENCRYPTION_KEY


class EncryptionService:
    @staticmethod
    def encrypt(string: str) -> str:
        fernet_key = bytes(ENCRYPTION_KEY, encoding='UTF-8')

        return Fernet(fernet_key).encrypt(bytes(string, encoding='UTF-8')).decode('UTF-8')

    @staticmethod
    def decrypt(bytes_string: str) -> str:
        fernet_key = bytes(ENCRYPTION_KEY, encoding='UTF-8')

        return Fernet(fernet_key).decrypt(bytes_string.encode('UTF-8')).decode('UTF-8')
