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
