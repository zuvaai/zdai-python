from .exceptions import ApiNoTokenError, ApiNoUrlError


class ApiAccess(object):
    """
    ApiAccess class holds the data required to access the Api
    """

    def __init__(self, token: str, url: str):
        self.token = token
        self.url = url

    @property
    def token(self) -> str:
        """
        Gets the Bearer Token
        :return:
        """
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        """
        Sets the token.

        :param value: The token
        :return:
        """
        if not value:
            raise ApiNoTokenError

        assert isinstance(value, str), f'Token must be provided as a string. Input: {value}'

        if not str(value).startswith('Bearer '):
            value = f'Bearer {value}'

        self._token = value

    @property
    def url(self) -> str:
        """
        Gets the base url of the destination.
        :return:
        """
        return self._url

    @url.setter
    def url(self, value: str) -> None:
        """
        Sets the base url of the destination.
        :param value:
        :return:
        """
        if not value:
            raise ApiNoUrlError

        assert isinstance(value, str), f'Url must be provided as a string. Input: {value}'

        if not str(value).endswith('/'):
            value = f'{value}/'

        self._url = value
