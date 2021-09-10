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

class BaseModel(object):
    """
    BaseModel contains the base methods of the ZDAI model
    """
    def __init__(self, json: dict):
        self._data = json

    def __repr__(self) -> str:
        _data = ', '.join("{}={!r}".format(k, v) for k, v in vars(self).get('_data').items())
        return f'{self.__class__.__name__}({_data})'

    def json(self) -> dict:
        """
        Returns the json data of the model
        """
        return self._data

    def is_done(self) -> bool:
        """
        If the model contains a status, returns if the model has completed or not
        """
        if not self._data.get('status'):
            pass

        return self._data.get('status') in ['failed', 'complete']

    def is_successful(self) -> bool:
        """
        Returns whether the status is set to 'complete' (i.e. a request that completed successfully).
        """
        return self._data.get('status') == 'complete'
