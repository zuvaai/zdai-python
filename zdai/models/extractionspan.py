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


class ExtractionSpan(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def start(self):
        return self.json().get('start')

    @property
    def end(self):
        return self.json().get('end')

    @property
    def page_start(self):
        return self.json().get('pages').get('start')

    @property
    def page_end(self):
        return self.json().get('pages').get('end')

    @property
    def top(self):
        return self.json().get('bounds').get('top')

    @property
    def left(self):
        return self.json().get('bounds').get('left')

    @property
    def bottom(self):
        return self.json().get('bounds').get('bottom')

    @property
    def right(self):
        return self.json().get('bounds').get('right')