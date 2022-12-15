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
from ..models.file import File, FileExpiration
from typing import Tuple
from datetime import datetime


class FileAPI(object):
    """
    FileAPI contains the functionality accepted by the File/Storage Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, content: bytes, is_zuva_ocr: bool = False, expiration: str = None) -> Tuple[File, ApiCall]:
        """
        Creates a new file in the ZDAI

        :param content: The byte-content of the data to submit.
        :param is_zuva_ocr: If the byte content provided comes from a .zuvaocr file.
        :param expiration: Set the expiration of the document. Defaults to 7d in DocAI. Max 13d.
        :return:
        """
        caller = self._call.new(method = 'POST', path = f'files')
        caller.use_default_accept_type = False
        caller.use_default_content_type = False
        if is_zuva_ocr: caller.add_header(key = 'Content-Type', value = 'application/eocr')
        if expiration: caller.add_header(key = 'Expiration', value = expiration)

        caller.set_body_value(value = content)
        caller.send()

        data = caller.response.json()

        file = File(
            id = data.get('file_id'),
            content_type = data.get('attributes').get('content-type'),
            expiration = datetime.strptime(data.get('expiration'), '%Y-%m-%dT%H:%M:%SZ')
        )

        return file, caller

    def delete(self, file_id: str) -> Tuple[bool, ApiCall]:
        """
        Deletes a file

        :return:
        """
        caller = self._call.new(method = 'DELETE', path = f'files/{file_id}')
        caller.send()

        return caller.response.status_code == 204, caller

    def set_expiration(self, file_id: str, expiration: str):
        """
        Sets the file expiration

        Example expirations are:
            2022-12-17T00:00:00Z — sets the expiration to December 17, 2022
            1d — sets the expiration to 1 day from when this call is run
            13d — sets the expiration to 13 days from when this all is run

        :param file_id: The file ID for which the file expiration will be set
        :param expiration: The new expiration (formatted YYYY-MM-DDTHH:mm:ssZ), or length of time (e.g. 7d for 7 days),
        :return: The file_id updated and the new expiration date
        """

        caller = self._call.new(method = 'PUT', path = f'files/{file_id}/expiration')
        caller.add_header(key = 'Expiration', value = expiration)
        caller.send()

        new_expiration = caller.response.json().get('expiration')
        if not new_expiration:
            raise Exception(f'No expiration found for file_id {file_id}.')

        new_expiration = datetime.strptime(new_expiration, "%Y-%m-%dT%H:%M:%SZ")

        return FileExpiration(id = caller.response.json().get('file_id'),
                              expiration = new_expiration), caller
