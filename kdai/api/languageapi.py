from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.language import Language


class LanguageAPI(object):
    """
    LanguageAPI contains the functionality accepted by the Language Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str]) -> Tuple[List[Language], ApiCall]:
        """
        Creates a new Language request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'language')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.send()

        return [Language(json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[Language, ApiCall]:
        """
        Gets the Language data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'language/{request_id}')
        caller.send()

        return Language(json = caller.response.json()), caller
