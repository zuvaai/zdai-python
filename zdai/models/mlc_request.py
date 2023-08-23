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


class MLCRequest(BaseRequest):
    def __init__(self, api, json):
        super().__init__(api = api, json = json)

    @property
    def classifications(self):
        return self.json().get('classifications')

    def has_classifications(self):
        return len(self.classifications) > 0

    def is_contract(self):
        if self.has_classifications():
            return self.classifications[0].lower() == 'contract'

        return None

    @property
    def classification_1(self):
        if self.has_classifications() and len(self.classifications) >= 1:
            return self.classifications[0]
        else:
            return None

    @property
    def classification_2(self):
        if self.has_classifications() and len(self.classifications) >= 2:
            return self.classifications[1]
        else:
            return None

    @property
    def classification_3(self):
        if self.has_classifications() and len(self.classifications) >= 3:
            return self.classifications[2]
        else:
            return None

    @property
    def language_name(self):
        return self.json().get('language').get('name')

    @property
    def language_code(self):
        return self.json().get('language').get('code')

    @property
    def is_amendment(self):
        return self.json().get('is_amendment')

    @property
    def is_master_agreement(self):
        return self.json().get('is_master_agreement')