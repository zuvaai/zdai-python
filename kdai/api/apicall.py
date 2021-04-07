import requests
from requests import Response

from .apiendpoint import ApiEndpoint
from .exceptions import *


class ApiCall(ApiEndpoint):
    """
    ApiCall class contains data relating to an ApiEndpoint's call.
    """

    def __init__(self, token=None, url=None, method=None, path=None):
        super().__init__(token = token, url = url)
        self._response = None

        if method: self.method = method
        if path: self.path = path

    def __repr__(self) -> str:
        data = ', '.join("{}={!r}".format(k, v) for k, v in vars(self).items())
        return f'{self.__class__.__name__}({data})'

    def new(self, method: str, path: str) -> 'ApiCall':
        return ApiCall(token = self.token, url = self.url, method = method, path = path)

    @property
    def response(self) -> Response:
        """
        Gets the Api response.

        :return:
        """
        return self._response

    @response.setter
    def response(self, response: Response) -> None:
        """
        Sets the Api response

        :param response:
        :return:
        """
        self._response = response

    def info(self) -> dict:
        return {'method': self.method,
                'url': self.uri,
                'params': self.parameters,
                'headers': self.headers,
                'data': self.body}

    def _check_for_exception(self):
        try:
            self.response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if self.response.status_code == 400:
                raise ApiCallBadRequestError(self)
            elif self.response.status_code == 403:
                raise ApiCallForbiddenError(self)
            elif self.response.status_code == 404:
                raise ApiCallNotFoundError(self)
            elif self.response.status_code == 409:
                raise ApiCallConflictError(self)
            elif self.response.status_code == 500:
                raise ApiCallInternalServerError(self)
            else:
                raise Exception(f'HTTP Error: {e}')
        except Exception as e:
            raise Exception(f'Exception: {e}')

    def send(self) -> None:
        """
        Calls the API Endpoint
        :return:
        """
        self.response = requests.request(method = self.method,
                                         params = self.parameters,
                                         headers = self.headers,
                                         url = self.uri,
                                         data = self.body)

        self._check_for_exception()
