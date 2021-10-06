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
from ..models.field import Field


class FieldAPI(object):
    """
    FieldAPI contains the functionality accepted by the Fields Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def get(self) -> Tuple[List[Field], ApiCall]:
        """
        Gets the list of fields that exist in the ZDAI, which
        the API token has access to.

        :return:
        """
        caller = self._call.new(method = 'GET', path = 'fields')
        caller.send()

        fields = []
        for field in caller.response.json():
            fields.append(Field(
                id = str(field.get('field_id')),
                name = str(field.get('name')),
                description = str(field.get('description')),
                bias = float(field.get('bias')),
                f_score = float(field.get('f_score')),
                precision = float(field.get('precision')),
                recall = float(field.get('recall')),
                document_count = int(field.get('document_count')),
                is_custom = bool(field.get('is_custom'))
            ))

        return fields, caller
