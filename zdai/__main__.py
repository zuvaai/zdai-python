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

from .config import config
from .ZDAISDK import ZDAISDK
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--get",
                    type = str,
                    choices = ["url", "token"],
                    help = 'Returns the default url used by the wrapper')
parser.add_argument("--set-token",
                    type = str,
                    help = 'Sets the default token')
parser.add_argument("--set-url",
                    type = str,
                    help = 'Sets the default url')
parser.add_argument("--test",
                    type = str,
                    choices = ["connection"],
                    help = 'Perform an test action')

args = parser.parse_args()

if __name__ == "__main__":
    url, token = config.get_access()

    if args.get == "token":
        if not token:
            print(f'No default token found')
        else:
            print(token)
    elif args.get == "url":
        if not url:
            print(f'No default url found')
        else:
            print(url)
    elif args.set_token:
        config.update_wrapper_config(token = args.set_token)
        print('Token set')
    elif args.set_url:
        config.update_wrapper_config(url = args.set_url)
        print('Url set')
    elif args.test == 'connection':
        if any(f == "" for f in [url, token]):
            print(f'Unable to perform connection test using default values: either url or token missing.')
            exit(1)

        sdk = ZDAISDK(from_config = True)

        try:
            fields, _ = sdk.fields.get()
            print(f'Connection test succeeded [Retrieved {len(fields)} fields]')
        except Exception as e:
            print(f'Connection test failed: {e}')
