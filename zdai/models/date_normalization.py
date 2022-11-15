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
class Date:
    day: int
    month: int
    year: int


class DateNormalization(BaseNormalization):
    def __init__(self, api, json):
        super().__init__(api = api, json = json)

    @property
    def _dates(self):
        return self.json().get('date')

    @property
    def dates(self):
        dates = []
        if not self._dates:
            return

        for date in self._dates:
            dates.append(Date(day = date.get('day'),
                              month = date.get('month'),
                              year = date.get('year')))

        return dates

