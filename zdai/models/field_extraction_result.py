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

from dataclasses import dataclass, field
from typing import List


@dataclass
class BoundingBox:
    """
    Dataclass to store a single bounding box
    """
    top: int = None
    left: int = None
    bottom: int = None
    right: int = None

    def __init__(self, bounds):
        self.top = bounds.top
        self.left = bounds.left
        self.bottom = bounds.bottom
        self.right = bounds.right


@dataclass
class BoundingBoxesByPage:
    """
    Dataclass to store the bounding boxes associated with a field extraction result span
    """
    page: int = None
    bounds: List[BoundingBox] = field(default_factory=lambda: [])

    def __init__(self, page_bounds):
        self.page = page_bounds.page
        self.bounds = [BoundingBox(line) for line in page_bounds.bounds]


@dataclass
class FieldExtractionResultSpan:
    """
    Dataclass to store the properties associated with a field extraction result span
    """
    confidence: float = None
    text_start: int = None
    text_end: int = None
    page_start: int = None
    page_end: int = None
    top: int = None
    left: int = None
    bottom: int = None
    right: int = None
    bboxes: List[BoundingBoxesByPage] = field(default_factory=lambda: [])


@dataclass
class FieldExtractionResultDefinedTerm:
    """
    Dataclass to store the properties associated with a field extraction result defined term
    """
    term: str = None
    spans: List[FieldExtractionResultSpan] = field(default_factory=lambda: [])


@dataclass
class CurrencyNormalizedValues:
    """
    Dataclass to store the normalized currency values
    """
    value: float = None
    symbol: str = None
    precision: int = None


@dataclass
class DateNormalizedValues:
    """
    Dataclass to store the normalized date values
    """
    day: int = None
    month: int = None
    year: int = None

@dataclass
class DurationNormalizedValues:
    """
    Dataclass to store the duration date values
    """
    unit: str = None
    value: int = None

@dataclass
class FieldExtractionResult:
    """
    Dataclass to store the properties associated with a field extraction result
    """
    field_id: str = None
    text: str = None
    spans: List[FieldExtractionResultSpan] = field(default_factory=lambda: [])
    defined_term: FieldExtractionResultDefinedTerm = None
    durations_normalized: List[DurationNormalizedValues] = field(default_factory=lambda: [])
    dates_normalized: List[DateNormalizedValues] = field(default_factory=lambda: [])
    currencies_normalized: List[CurrencyNormalizedValues] = field(default_factory=lambda: [])

    def is_normalized(self):
        return any([self.durations_normalized, self.dates_normalized, self.currencies_normalized])

    def get_normalized(self):
        if not self.is_normalized():
            return None, None

        if self.durations_normalized:
            return 'durations', self.durations_normalized
        elif self.dates_normalized:
            return 'dates', self.dates_normalized
        elif self.currencies_normalized:
            return 'currencies', self.currencies_normalized
