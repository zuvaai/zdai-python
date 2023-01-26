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

from .basenormalization import BaseNormalization
from dataclasses import dataclass

@dataclass
class Currency:
    value: float
    symbol: str
    precision: int


class CurrencyNormalization(BaseNormalization):
    def __init__(self, api, json):
        super().__init__(api = api, json = json)

    @property
    def _currencies(self):
        return self.json().get('currency')

    @property
    def currencies(self):
        currencies = []
        for currency in self._currencies:
            currencies.append(Currency(value = currency.get('value'),
                                       symbol = currency.get('symbol'),
                                       precision = currency.get('precision')))

        return currencies
