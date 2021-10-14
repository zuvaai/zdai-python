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

from .baserequest import BaseRequest


class OCRRequest(BaseRequest):
    def __init__(self, api, json):
        super().__init__(api = api, json = json)

    def get_text(self):
        result, _ = self.api().get_text(request_id = self.id)
        return result.get('text')

    def get_images(self):
        data = self.api().get_images(request_id = self.id)
        return data
