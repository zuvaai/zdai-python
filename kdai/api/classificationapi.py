from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.classification import Classification


class ClassificationAPI(object):
    """
    ClassificationAPI contains the functionality accepted by the Classification Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str]) -> Tuple[List[Classification], ApiCall]:
        """
        Creates a new classification request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'classification')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.send()

        return [Classification(json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[Classification, ApiCall]:
        """
        Gets the Classification data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'classification/{request_id}')
        caller.send()

        return Classification(json = caller.response.json()), caller
