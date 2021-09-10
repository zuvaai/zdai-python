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

from ..api.apicall import ApiCall
from ..models.file import File
from typing import Tuple


class FileAPI(object):
    """
    FileAPI contains the functionality accepted by the File/Storage Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, content: bytes, is_zuva_ocr: bool = False) -> Tuple[File, ApiCall]:
        """
        Creates a new file in the ZDAI

        :param content: The byte-content of the data to submit.
        :param is_zuva_ocr: If the byte content provided comes from a .zuvaocr file.
        :return:
        """
        caller = self._call.new(method = 'POST', path = f'files')
        caller.use_default_accept_type = False
        caller.use_default_content_type = False
        if is_zuva_ocr: caller.add_header(key = 'Content-Type', value = 'application/kiraocr')
        caller.set_body_value(value = content)
        caller.send()

        return File(json = caller.response.json()), caller

    def delete(self, file_id: int) -> Tuple[bool, ApiCall]:
        """
        Deletes a file

        :return:
        """
        caller = self._call.new(method = 'DELETE', path = f'files/{file_id}')
        caller.send()

        return caller.response.status_code == 204, caller
