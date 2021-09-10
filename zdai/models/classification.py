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

from .basemodel import BaseModel


class Classification(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def file_id(self) -> str:
        return self.json().get('file_id')

    @property
    def status(self) -> str:
        return self.json().get('status')

    @property
    def request_id(self) -> str:
        return self.json().get('request_id')

    @property
    def classification(self) -> str:
        return self.json().get('classification')

    @property
    def is_contract(self) -> bool:
        is_contract = self.json().get('is_contract')

        if is_contract:
            if isinstance(is_contract, bool):
                return bool(is_contract)
            else:
                raise Exception(f'Unexpected non-boolean is_contract: {is_contract}')
