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

from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.language_classification_request import LanguageClassificationRequest


class LanguageAPI(object):
    """
    LanguageAPI contains the functionality accepted by the Language Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str]) -> Tuple[List[LanguageClassificationRequest], ApiCall]:
        """
        Creates a new Language request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'language')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.send()

        return [LanguageClassificationRequest(api = self, json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[LanguageClassificationRequest, ApiCall]:
        """
        Gets the Language data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'language/{request_id}')
        caller.send()

        return LanguageClassificationRequest(api = self, json = caller.response.json()), caller

    def get_multiple(self, request_ids: List[str]) -> Tuple[List[LanguageClassificationRequest], ApiCall]:
        """
        Gets multiple Language statuses

        """
        caller = self._call.new(method='GET', path=f'languages')
        caller.add_parameter('request_id', request_ids)
        caller.send()

        language_requests = []

        for request_id, result in caller.response.json().get('statuses').items():
            r = result
            r['request_id'] = request_id
            language_requests.append(LanguageClassificationRequest(api = self, json = r))

        return language_requests, caller