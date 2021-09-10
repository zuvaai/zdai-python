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

from .apicall import ApiCall
from ..models.extraction import Extraction


class ExtractionAPI(object):
    """
    ExtractionAPI contains the functionality accepted by the Extraction Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str], field_ids: List[str]) -> Tuple[List[Extraction], ApiCall]:
        """
        Creates a new extraction request for the file ids and field ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'extraction')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.add_body(key = 'field_ids', value = field_ids)
        caller.send()

        return [Extraction(json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[Extraction, ApiCall]:
        """
        Gets the Extraction Status data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}')
        caller.send()

        return Extraction(json = caller.response.json()), caller

    def get_result(self, request_id: str) -> Tuple[Extraction, ApiCall]:
        """
        Gets the Extraction Result data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}/results/text')
        caller.send()

        return Extraction(json = caller.response.json()), caller
