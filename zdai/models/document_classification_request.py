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


class DocumentClassificationRequest(BaseRequest):
    """
    The class used for requests created in the Document Classification service
    """
    def __init__(self, api, json):
        super().__init__(api = api, json = json)

    def is_contract(self):
        """
        Returns whether or not the document is a contract
        """
        return self.json().get('is_contract')

    def classification(self):
        """
        Returns the type of document that was provided
        """
        return self.json().get('classification')
