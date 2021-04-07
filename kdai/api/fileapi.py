from ..api.apicall import ApiCall
from ..models.file import File
from typing import Tuple


class FileAPI(object):
    """
    FileAPI contains the functionality accepted by the File/Storage Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, content: bytes, is_kira_ocr: bool = False) -> Tuple[File, ApiCall]:
        """
        Creates a new file in the KDAI

        :param content: The byte-content of the data to submit.
        :param is_kira_ocr: If the byte content provided comes from a .kiraocr file.
        :return:
        """
        caller = self._call.new(method = 'POST', path = f'files')
        caller.use_default_accept_type = False
        caller.use_default_content_type = False
        if is_kira_ocr: caller.add_header(key = 'Content-Type', value = 'application/kiraocr')
        caller.set_body_value(value = content)
        caller.send()

        return File(json = caller.response.json()), caller

    def delete(self, file_id: int) -> Tuple[bool, ApiCall]:
        """
        Deletes a file

        :return:
        """
        caller = self._call.new(method = 'DELETE', path = f'files/{file_id}')
        caller.send()

        return caller.response.status_code == 204, caller
