import json


def _get_error_data(content):
    if not content:
        return None, None

    try:
        _content = json.loads(content)
    except Exception as e:
        return None, str(content)

    if _content.get('error'):
        error_code = _content.get('error').get('code')
        error_message = _content.get('error').get('message')
        return error_code, error_message
    else:
        error_code = _content.get('code')
        error_message = _content.get('message')
        return error_code, error_message


class ApiCallError(Exception):  # , formatted_message: str, error_message: str = None, error_code: str = None
    def __init__(self, call):
        self.call = call
        super().__init__(self.formatted_message)


class ApiCallBadRequestError(ApiCallError):
    def __init__(self, call):
        self.call = call
        self.error_code, self.error_message = _get_error_data(call.response.content)
        # self.error_code = json.loads(call.response.content).get('error').get('code')
        # self.error_message = json.loads(call.response.content).get('error').get('message')
        self.formatted_message = f'Bad Request: {self.error_code}: {self.error_message}'
        super().__init__(call)


class ApiCallForbiddenError(ApiCallError):
    def __init__(self, call):
        self.call = call
        self.error_code, self.error_message = _get_error_data(call.response.content)
        # self.error_code = json.loads(call.response.content).get('error').get('code')
        # self.error_message = json.loads(call.response.content).get('error').get('message')
        self.formatted_message = f'Forbidden: {self.error_code}: {self.error_message}'
        super().__init__(call)


class ApiCallNotFoundError(ApiCallError):  # catch-all exception
    def __init__(self, call):
        self.call = call
        self.error_code, self.error_message = _get_error_data(call.response.content)
        self.formatted_message = f'Not Found: {call.response.request.url}'
        super().__init__(call)


class ApiCallConflictError(ApiCallError):
    def __init__(self, call):
        self.call = call
        self.error_code, self.error_message = _get_error_data(call.response.content)
        # self.error_code = json.loads(call.response.content).get('error').get('code')
        # self.error_message = json.loads(call.response.content).get('error').get('message')
        self.formatted_message = f'Conflict: {self.error_code}: {self.error_message}'
        super().__init__(call)


class ApiCallInternalServerError(ApiCallError):
    def __init__(self, call):
        self.call = call
        self.error_code, self.error_message = _get_error_data(call.response.content)
        # self.error_code = json.loads(call.response.content).get('code')
        # self.error_message = json.loads(call.response.content).get('message')
        self.formatted_message = f'Internal Server Error: {self.error_code}: {self.error_message}'
        super().__init__(call)

class ApiNoTokenError(Exception):
    def __init__(self):
        message = 'No token provided'
        super().__init__(message)


class ApiNoUrlError(Exception):
    def __init__(self):
        message = 'No url provided'
        super().__init__(message)


class ApiNoAccessProvidedError(Exception):
    def __init__(self, url: str, token: str):
        message = f'No Access Provided: A token and url are required. [URL: {url}, Token: {token}]'
        super().__init__(message)
