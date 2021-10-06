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

from datetime import datetime
from dataclasses import dataclass


@dataclass
class File:
    id: str
    content_type: str
    expiration: datetime

    def is_pdf(self):
        return 'application/pdf' in self.content_type

    def is_text(self):
        return 'text/plain' in self.content_type

    def is_zuva_ocr(self):
        return 'appliation/kiraocr' in self.content_type

