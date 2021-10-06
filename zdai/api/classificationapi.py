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
from ..models.document_classification_request import DocumentClassificationRequest


class ClassificationAPI(object):
    """
    ClassificationAPI contains the functionality accepted by the Classification Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str]) -> Tuple[List[DocumentClassificationRequest], ApiCall]:
        """
        Creates a new classification request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'classification')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.send()

        return [DocumentClassificationRequest(api = self, json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[DocumentClassificationRequest, ApiCall]:
        """
        Gets the Classification data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'classification/{request_id}')
        caller.send()

        return DocumentClassificationRequest(api = self, json = caller.response.json()), caller
