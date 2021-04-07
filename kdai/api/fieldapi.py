from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.field import Field


class FieldAPI(object):
    """
    FieldAPI contains the functionality accepted by the Fields Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def get(self) -> Tuple[List[Field], ApiCall]:
        """
        Gets the list of fields that exist in the KDAI, which
        the API token has access to.

        :return:
        """
        caller = self._call.new(method = 'GET', path = 'fields')
        caller.send()

        return [Field(json = f) for f in caller.response.json()], caller
