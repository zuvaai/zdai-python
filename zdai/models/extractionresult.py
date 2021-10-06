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
from .extractionspan import ExtractionSpan


class ExtractionResult(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def text(self):
        return self.json().get('text')

    @property
    def spans(self):
        spans = self.json().get('spans')
        _e = []
        if spans:
            for _extraction in spans:
                _e.append(ExtractionSpan(_extraction))
        return _e