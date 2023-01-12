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

import zdai as zdai
from .api.exceptions import ApiNoAccessProvidedError


class ZDAISDK(object):
    """
    Zuva Document AI (ZDAI) SDK which acts as an entry-point to get an instance of
    an API class that's associated to a ZDAI microservice.
    """

    def __init__(self, url: str = None, token: str = None, from_config=False):
        self.url = url
        self.token = token

        if from_config:
            self.url, self.token = zdai.config.get_access()

        if not self.has_access():
            raise ApiNoAccessProvidedError(url = self.url, token = self.token)

        self._load_apis()

    def _load_apis(self):
        self._file_api = zdai.FileAPI(url = self.url, token = self.token)
        self._classification_api = zdai.ClassificationAPI(url = self.url, token = self.token)
        self._language_api = zdai.LanguageAPI(url = self.url, token = self.token)
        self._extraction_api = zdai.ExtractionAPI(url = self.url, token = self.token)
        self._field_api = zdai.FieldAPI(url = self.url, token = self.token)
        self._ocr_api = zdai.OCRAPI(url = self.url, token = self.token)
        self._mlc_api = zdai.MLCAPI(url = self.url, token = self.token)
        self._normalization_api = zdai.NormalizationAPI(url = self.url, token = self.token)

    def has_access(self):
        return all(f is not None for f in [self.url, self.token])

    @property
    def file(self) -> zdai.FileAPI:
        """
        Returns the FileAPI instance
        """
        return self._file_api

    @property
    def classification(self) -> zdai.ClassificationAPI:
        """
        Returns the ClassificationAPI instance
        """
        return self._classification_api

    @property
    def language(self) -> zdai.LanguageAPI:
        """
        Returns the LanguageAPI instance
        """
        return self._language_api

    @property
    def extraction(self) -> zdai.ExtractionAPI:
        """
        Returns the ExtractionAPI instance
        """
        return self._extraction_api

    @property
    def fields(self) -> zdai.FieldAPI:
        """
        Returns the FieldAPI instance
        """
        return self._field_api

    @property
    def ocr(self) -> zdai.OCRAPI:
        """
        Returns the OCRAPI instance
        """
        return self._ocr_api

    @property
    def mlc(self) -> zdai.MLCAPI:
        """
        Returns the MLCAPI instance
        """
        return self._mlc_api

    @property
    def normalization(self) -> zdai.NormalizationAPI:
        """
        Returns the Normalization instance
        """
        return self._normalization_api

    @property
    def config(self):
        """
        Returns the config
        """
        return zdai.config
