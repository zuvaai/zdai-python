from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.ocr import OCR


class OCRAPI(object):
    """
    OCRAPI contains the functionality accepted by the OCR Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str]) -> Tuple[List[OCR], ApiCall]:
        """
        Creates a new OCR request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'ocr')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.send()

        return [OCR(json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[OCR, ApiCall]:
        """
        Gets the OCR status for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}')
        caller.send()

        return OCR(json = caller.response.json()), caller

    def get_text(self, request_id: str) -> Tuple[OCR, ApiCall]:
        """
        Gets the OCR text for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/text')
        caller.send()

        return OCR(json = caller.response.json()), caller

    def get_images(self, request_id: str, ) -> 'ApiCall':
        """
        Gets the bytes of a .zip package which contains all of the images.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/images')
        caller.send()

        return caller
