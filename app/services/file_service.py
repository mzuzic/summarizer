import os
import tempfile


class FileService:
    def get_file_extension(self, file):
        _, file_extension = os.path.splitext(file.file_path)

        return file_extension

    def store_in_temp_file(self, temp_file, document_file):
        os.write(temp_file, document_file.read())
        os.close(temp_file)


class TemporaryFile:
    def __init__(self, name, doc_type):
        self.file, self.file_path = tempfile.mkstemp(prefix=name, suffix=doc_type)
