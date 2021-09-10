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


class Field(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def id(self) -> str:
        return self.json().get('field_id')

    @property
    def name(self) -> str:
        return self.json().get('name')

    @property
    def description(self) -> str:
        return self.json().get('description')

    @property
    def bias(self) -> float:
        return float(self.json().get('bias'))

    @property
    def fscore(self) -> float:
        return float(self.json().get('f_score'))

    @property
    def precision(self) -> float:
        return float(self.json().get('precision'))

    @property
    def recall(self) -> float:
        return float(self.json().get('recall'))

    @property
    def document_count(self) -> int:
        return int(self.json().get('document_count'))

    @property
    def is_custom(self):
        return bool(self.json().get('is_custom'))
