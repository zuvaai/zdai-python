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
from ..models.ocr_request import OCRRequest


class OCRAPI(object):
    """
    OCRAPI contains the functionality accepted by the OCR Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str], generate_layout: bool = None) -> Tuple[List[OCRRequest], ApiCall]:
        """
        Creates a new OCR request for the file ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'ocr')
        caller.add_body(key = 'file_ids', value = file_ids)
        if generate_layout != None:
            caller.add_body(key = 'layout', value = generate_layout)

        caller.send()

        return [OCRRequest(api = self, json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[OCRRequest, ApiCall]:
        """
        Gets the OCR status for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}')
        caller.send()

        return OCRRequest(api = self, json = caller.response.json()), caller

    def get_multiple(self, request_ids: List[str]) -> Tuple[List[OCRRequest], ApiCall]:
        """
        Gets multiple OCR statuses

        """
        caller = self._call.new(method= 'GET', path=f'ocrs')
        caller.add_parameter('request_id', request_ids)
        caller.send()

        ocr_requests = []

        for request_id, result in caller.response.json().get('statuses').items():
            result['request_id'] = request_id
            ocr_requests.append(OCRRequest(api = self, json = result))

        return ocr_requests, caller

    def get_text(self, request_id: str) -> Tuple[dict, ApiCall]:
        """
        Gets the OCR text for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/text')
        caller.send()

        return caller.response.json(), caller

    def get_images(self, request_id: str, ) -> 'ApiCall':
        """
        Gets the bytes of a .zip package which contains all of the images.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/images')
        caller.send()

        return caller

    def get_eocr(self, request_id: str) -> 'ApiCall':
        """
        Gets the file's layout in eOCR format

        :return:
        """

        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/eocr')
        caller.send()

        return caller

    def get_layouts(self, request_id: str) -> 'ApiCall':
        """
        Gets the file's protobuf layout

        :return:
        """

        caller = self._call.new(method = 'GET', path = f'ocr/{request_id}/layouts')
        caller.send()

        return caller

    def get_layout(self, request_id: str) -> 'ApiCall':
        """
        Gets the file's protobuf layout (backwards compatibility)

        :return:
        """
        return self.get_layouts(request_id)
