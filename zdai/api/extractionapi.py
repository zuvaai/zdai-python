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
from ..models.field_extraction_request import FieldExtractionRequest
from ..models.field_extraction_result import FieldExtractionResult, FieldExtractionResultSpan
import json
from types import SimpleNamespace


class ExtractionAPI(object):
    """
    ExtractionAPI contains the functionality accepted by the Extraction Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, file_ids: List[str], field_ids: List[str]) -> Tuple[List[FieldExtractionRequest], ApiCall]:
        """
        Creates a new extraction request for the file ids and field ids provided.

        :return:
        """
        caller = self._call.new(method = 'POST', path = 'extraction')
        caller.add_body(key = 'file_ids', value = file_ids)
        caller.add_body(key = 'field_ids', value = field_ids)
        caller.send()

        return [FieldExtractionRequest(api = self, json = c) for c in caller.response.json().get('file_ids')], caller

    def get(self, request_id: str) -> Tuple[FieldExtractionRequest, ApiCall]:
        """
        Gets the Extraction Status data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}')
        caller.send()

        return FieldExtractionRequest(api = self, json = caller.response.json()), caller

    def get_result(self, request_id: str) -> Tuple[List[FieldExtractionResult], ApiCall]:
        """
        Gets the Extraction Result data for the request_id.

        :return:
        """
        caller = self._call.new(method = 'GET', path = f'extraction/{request_id}/results/text')
        caller.send()

        data = json.dumps(caller.response.json())

        namespaces = json.loads(data, object_hook = lambda d: SimpleNamespace(**d))

        results = []

        # Go through each of the Extraction Results
        for result in namespaces.results:

            # If there's no extracted data for the Field, then append an empty field extraction result
            if not result.extractions:
                # Regardless if there's extracted text, tag each result with a field_id.
                results.append(FieldExtractionResult(field_id = result.field_id))
                continue

            # If there's extracted data for the Field, then create a new instance of FieldExtractionResult
            # for each of the entries. Append the spans list for each text extraction.
            for extraction in result.extractions:
                extraction_result = FieldExtractionResult(field_id = result.field_id)

                extraction_result.text = extraction.text

                for span in extraction.spans:
                    extraction_span = FieldExtractionResultSpan(
                                                text_start = span.start,
                                                text_end = span.end,
                                                page_start = span.pages.start,
                                                page_end = span.pages.end,
                                                top = span.bounds.top,
                                                left = span.bounds.left,
                                                bottom = span.bounds.bottom,
                                                right = span.bounds.right)

                    extraction_result.spans.append(extraction_span)
                results.append(extraction_result)

        return results, caller
