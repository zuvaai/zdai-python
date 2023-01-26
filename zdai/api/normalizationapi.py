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

from typing import Tuple

from ..api.apicall import ApiCall
from ..models.date_normalization import DateNormalization
from ..models.currency_normalization import CurrencyNormalization
from ..models.duration_normalization import DurationNormalization


class NormalizationAPI(object):
    """
    NormalizationAPI contains the functionality accepted by the Normalization services
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def get_dates(self, text: str) -> Tuple[DateNormalization, ApiCall]:
        """
        Gets the normalized date values from the input string

        :return:
        """

        caller = self._call.new(method = 'POST', path = 'normalize/date')
        caller.add_body(key = 'text', value = text)
        caller.send()

        return DateNormalization(api = self, json = caller.response.json()), caller

    def get_durations(self, text: str) -> tuple[DurationNormalization, ApiCall]:
        """
        Gets the normalized duration values from the input string

        :return:
        """

        caller = self._call.new(method = 'POST', path = 'normalize/duration')
        caller.add_body(key = 'text', value = text)
        caller.send()

        return DurationNormalization(api = self, json = caller.response.json()), caller

    def get_currencies(self, text: str) -> Tuple[CurrencyNormalization, ApiCall]:
        """
        Gets the normalized currency values from the input string

        :return:
        """

        caller = self._call.new(method = 'POST', path = 'normalize/currency')
        caller.add_body(key = 'text', value = text)
        caller.send()

        return CurrencyNormalization(api = self, json = caller.response.json()), caller
