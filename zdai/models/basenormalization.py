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


class BaseNormalization:
    def __init__(self, api, json):
        self._type = type(self)
        self._api = api
        self._json = json

    def json(self):
        return self._json

    @property
    def request_id(self):
        return self.json().get('request_id')

    @property
    def text(self):
        return self.json().get('text')

    @property
    def sha256(self):
        return self.json().get('sha-256')
