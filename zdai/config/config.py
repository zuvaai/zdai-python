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

import json
import os
import shutil


def _get_config_data(config_name):
    fullname = os.path.join(os.path.dirname(__file__), config_name)

    if not os.path.exists(fullname):
        return {}
    else:
        with open(fullname, 'r') as file:
            config = json.load(file)

        return config


def get_access_config():
    config = _get_config_data('access.json')
    return config


def get_access():
    config = get_access_config()
    url = config.get('url')
    token = config.get('token')
    return url, token


def update_wrapper_config(token: str = None, url: str = None):
    config = get_access_config()
    _file = os.path.join(os.path.dirname(__file__), 'access.json')

    if token:
        config['token'] = token
    if url:
        config['url'] = url

    with open(_file, "w") as file:
        json.dump(config, file, indent = 4)
