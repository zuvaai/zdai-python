from typing import List, Tuple

from .apicall import ApiCall
from ..models.extraction import Extraction


class ExtractionAPI(object):
    """
    ExtractionAPI contains the functionality accepted by the Extraction Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str], field_ids: List[str]) -> Tuple[List[Extraction], ApiCall]:
        """
        Creates a new extraction request for the file ids and field ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'extraction')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.add_body(key = 'field_ids', value = field_ids)
        caller.send()

        return [Extraction(json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[Extraction, ApiCall]:
        """
        Gets the Extraction Status data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}')
        caller.send()

        return Extraction(json = caller.response.json()), caller

    def get_result(self, request_id: str) -> Tuple[Extraction, ApiCall]:
        """
        Gets the Extraction Result data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}/results/text')
        caller.send()

        return Extraction(json = caller.response.json()), caller
