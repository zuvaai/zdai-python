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

from typing import List, Tuple

from ..api.apicall import ApiCall
from ..models.field import Field
from ..models.field_training import FieldValidationLocation, FieldValidationDetails, FieldMetadata, FieldAccuracy
from ..models.field_training_request import FieldTrainingRequest


class FieldAPI(object):
    """
    FieldAPI contains the functionality accepted by the Fields Microservice
    """

    def __init__(self, token: str, url: str):
        self._call = ApiCall(token, url)

    def create(self, field_name: str, description: str = None, from_field_id: str = None) -> Tuple[str, ApiCall]:
        """
        Creates a new field
        """
        caller = self._call.new(method='POST', path='fields')
        caller.add_body(key='field_name', value=field_name)

        if description:
            caller.add_body(key='description', value=description)

        if from_field_id:
            caller.add_body(key='from_field_id', value=from_field_id)

        caller.send()

        return caller.response.json().get('field_id'), caller

    def train(self, field_id: str, annotations: List[dict]):
        """
        Creates a field training  for the annotations provided.

        Annotations are provided in the following format:

            [
                {
                    "file_id": "",
                    "locations": [
                        {
                            "start": 0,
                            "end": 1
                        },
                        {
                            "start": 2,
                            "end": 3
                        }
                    ]
                }
            ]

        """
        caller = self._call.new(method='POST', path=f'fields/{field_id}/train')
        caller.set_body_value(annotations)
        caller.send()

        return FieldTrainingRequest(api=self, json=caller.response.json()), caller

    def get_training_status(self, field_id: str, request_id: int):
        """
        Obtain the latest status of the Field Training Request
        """
        caller = self._call.new(
            method='GET', path=f'fields/{field_id}/train/{request_id}')
        caller.send()

        return FieldTrainingRequest(api=self, json=caller.response.json()), caller

    def get(self) -> Tuple[List[Field], ApiCall]:
        """
        Gets the list of fields that exist in the ZDAI, which
        the API token has access to.
        """
        caller = self._call.new(method='GET', path='fields')
        caller.send()

        fields = []
        for field in caller.response.json():
            fields.append(Field(
                id=str(field.get('field_id')),
                name=str(field.get('name')),
                description=str(field.get('description')),
                bias=float(field.get('bias', 0.0)),
                f_score=float(field.get('f_score', 0.0)),
                precision=float(field.get('precision', 0.0)),
                recall=float(field.get('recall', 0.0)),
                document_count=int(field.get('document_count', 0)),
                is_custom=bool(field.get('is_custom')),
                has_answers=bool(field.get('has_answers'))
            ))

        return fields, caller

    def get_metadata(self, field_id: str):
        """
        Gets the field's metadata
        """

        caller = self._call.new(
            method='GET', path=f'fields/{field_id}/metadata')
        caller.send()

        return FieldMetadata(**caller.response.json()), caller

    def update_metadata(self, field_id: str, name: str, description: str):
        """
        Updates the field's metadata
        """

        caller = self._call.new(
            method='PUT', path=f'fields/{field_id}/metadata')
        caller.add_body(key='name', value=name)
        caller.add_body(key='description', value=description)
        caller.send()

        return caller.response.status_code == 204, caller

    def get_accuracy(self, field_id: str):
        """
        Gets the field's accuracy (precision, recall, fscore)
        """

        caller = self._call.new(
            method='GET', path=f'fields/{field_id}/accuracy')
        caller.send()

        return FieldAccuracy(**caller.response.json()), caller

    def get_validation_details(self, field_id: str):
        """
        Gets the field's validation details (type of instance (true positive, false positive, false negative) & location)
        """

        caller = self._call.new(
            method='GET', path=f'fields/{field_id}/validation-details')
        caller.send()

        response = caller.response.json()
        validation_details = []

        for validation_detail in response:
            location = FieldValidationLocation(character_start=validation_detail.get('location')[0],
                                               character_end=validation_detail.get('location')[1])

            v = FieldValidationDetails(file_id=validation_detail.get('file_id'),
                                       type=validation_detail.get('type'),
                                       location=location)

            validation_details.append(v)

        return validation_details, caller
