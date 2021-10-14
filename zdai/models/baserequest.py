# Copyright 2021 Zuva Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

class BaseRequest:
    """
    The BaseRequest class for the Zuva DocAI requests
    """
    def __init__(self, api, json):
        self._type = type(self)
        self._api = api
        self._json = json

    @property
    def type(self):
        """
        Returns the name of the class
        """
        return self._type.__name__

    @property
    def id(self):
        """
        Returns the request identifier
        """
        return self._json.get('request_id')

    @property
    def file_id(self):
        """
        Returns the file_id associated with the request
        """
        return self._json.get('file_id')

    @property
    def status(self):
        """
        Returns the status of the request
        This is only updated when the update() is run, or set_json() is used
        """
        return self._json.get('status')

    def json(self):
        """
        Returns the raw json of the request
        """
        return self._json

    def api(self):
        """
        Returns the instance of the API class
        For example: ClassificationAPI, LanguageAPI, OCIAPI, ExtractionAPI
        """
        return self._api

    def is_type(self, request_type):
        """
        Returns whether or not the provided request type is the same as this request
        This can be used when you create a list that contains multiple different types
        of requests, since each request type returns different values.
        For example: a Document Classification request can return 'classification' and
        'is_contract', which the Language Classification request wouldn't have.
        """
        return request_type == self._type

    def is_finished(self):
        """
        Returns whether or not the request completed processing
        """
        return self.status in ['complete', 'failed']

    def is_successful(self):
        """
        Returns whether or not the request has completed successfully
        """
        return self.status == 'complete'

    def is_failed(self):
        """
        Returns whether or not the request has completed unsuccessfully
        """
        return self.status == 'failed'

    def is_processing(self):
        """
        Returns whether or not the request is still processing
        """
        return self.status == 'processing'

    def is_queued(self):
        """
        Returns whether or not the request is queued
        """
        return self.status == 'queued'

    def update(self):
        """
        Updates the request with its latest status
        """
        latest, call = self.api().get(request_id = self.id)
        self._json = latest.json()
