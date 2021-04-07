from typing import Union, List
import json

from .apiaccess import ApiAccess


class ApiEndpoint(ApiAccess):
    """
    ApiEndpoint contains an Endpoint's main components needed to perform a call
    """

    def __init__(self, token=None, url=None):
        super().__init__(token = token, url = url)
        self.requires_token = True
        self.use_default_content_type = True
        self.default_content_type = 'application/json'
        self.use_default_accept_type = True
        self.default_accept_type = 'application/json'

        self._method = None
        self._path = None
        self._headers = {}
        self._parameters = {}
        self._body = {}

    @property
    def method(self) -> str:
        """
        Gets the endpoint's HTTP Method
        :return:
        """
        return self._method

    @method.setter
    def method(self, value: str) -> None:
        """
        Sets the endpoint's HTTP Method

        :param value: HTTP Method
        :return:
        """
        _value = str(value).upper()

        if _value not in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE']:
            raise Exception(f'Error setting the ApiEndpoint.Method to \'{value}\': Invalid method.')

        self._method = _value

    @property
    def path(self) -> str:
        """
        Gets the Path

        :return:
        """
        return self._path

    @path.setter
    def path(self, path: str) -> None:
        """
        Sets the path of the resource
        :param path:
        :return:
        """
        self._path = path

    @property
    def uri(self) -> str:
        """
        Gets the full uri of the endpoint (url + path)

        :return:
        """
        if not self._path:
            raise Exception('No URI path provided')

        return f'{self.url}{self.path}'

    @property
    def headers(self) -> dict:
        """
        Gets the endpoint's request headers.
        If the endpoint requires a token, then this will add the Authorization
        key and the Bearer Token to the headers.

        :return:
        """
        # Return the headers with the Authorization if self.requires_token is True.
        # Otherwise, don't include Authorization.
        if 'Authorization' not in self._headers and self.requires_token:
            self._headers['Authorization'] = self.token

        if 'Content-Type' not in self._headers and self.use_default_content_type:
            self._headers['Content-Type'] = self.default_content_type

        if 'Accept' not in self._headers and self.use_default_accept_type:
            self._headers['Accept'] = self.default_accept_type

        return self._headers

    def add_header(self, key: str, value: str) -> None:
        """
        Adds a new key/value pair to the endpoint's headers.

        :param key: The key name
        :param value: The value associated to the key
        :return:
        """
        self._headers[key] = value

    @property
    def parameters(self) -> dict:
        """
        Gets the endpoint's parameters.

        :return:
        """
        return self._parameters

    def add_parameter(self, key: str, value: object) -> None:
        """
        Adds a new key/value pair to the endpoint's parameters.

        :param key: The key name
        :param value: The value associated to the key
        :return:
        """
        self._parameters[key] = value

    @property
    def body(self) -> Union[bytes, str, dict]:
        """
        Gets the endpoint's body

        :return:
        """
        return json.dumps(self._body) if isinstance(self._body, dict) else self._body

    def set_body_value(self, value: object) -> None:
        """
        Sets the value of the body. To be used if the body should contain anything but
        a dictionary.

        :param value: The content to populate the body with.
        :return:
        """
        if self._body:
            raise Exception(f'Unable to add value to body: body is already populated with a value.')

        self._body = value

    def add_body(self, key: str, value: Union[List, str]):
        """
        Adds a new key/value pair to the endpoint's body. To be used if you want
        to add data to the body, of type dictionary.

        :param key: The key name
        :param value: The value associated to the key
        :return:
        """
        if not isinstance(self._body, dict):
            raise Exception(f'Unable to add {key}/{value} to body: body is not a dictionary.')

        self._body[key] = value

    def add_kwargs(self, kwarg,
                   parameter_keys: list = None,
                   body_keys: list = None,
                   header_keys: list = None) -> None:
        """
        Parses the provided keyword-arguments into the headers, parameters or body.

        :param kwarg: the list of key/value pairs.
        :param parameter_keys: the kwarg's keys that exist in here will be added to the endpoint parameters
        :param body_keys: the kwarg's keys that exist in here will be added to the endpoint body
        :param header_keys: the kwarg's keys that exist in here will be added to the endpoint headers

        :return:
        """
        _parameter_keys = parameter_keys if parameter_keys is not None else []
        _body_keys = body_keys if body_keys is not None else []
        _header_keys = header_keys if header_keys is not None else []

        for key, value in kwarg.items():
            if key in _parameter_keys:
                self.add_parameter(key, value)
            elif key in _body_keys:
                self.add_body(key = key, value = value)
            elif key in _header_keys:
                self.add_header(key, value)
