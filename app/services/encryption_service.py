from cryptography.fernet import Fernet

from app.config.common import ENCRYPTION_KEY
from app.constants import UTF8


class EncryptionService:
    @staticmethod
    def encrypt(string: str) -> str:
        fernet_key = bytes(ENCRYPTION_KEY, encoding=UTF8)

        return Fernet(fernet_key).encrypt(bytes(string, encoding=UTF8)).decode(UTF8)

    @staticmethod
    def decrypt(bytes_string: str) -> str:
        fernet_key = bytes(ENCRYPTION_KEY, encoding=UTF8)

        return Fernet(fernet_key).decrypt(bytes_string.encode(UTF8)).decode(UTF8)
