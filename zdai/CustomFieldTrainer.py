from zdai import ZDAISDK
import time
import json


class CustomFieldTrainer(object):
    """
    The CustomFieldTrainer class can be used to create new custom fields using the DocAI
    Training APIs.

    Example usage:

        custom_field = CustomFieldTrainer(sdk = ZDAISDK(from_config = True), name = 'customfieldname')
        custom_field.create_empty()
        custom_field.add_annotation(file_id = 'abc', start = 100, end = 150)
        custom_field.add_annotation(file_id = 'abc', start = 500, end = 550)
        custom_field.train()
        print(custom_field.get_accuracy())
        print(custom_field.get_validation_details())
        print(custom_field.get_layout())
        print(custom_field.get_metadata())
    """
    def __init__(self, sdk: ZDAISDK, name: str, field_id: str = None):
        self.name = name
        self._sdk = sdk
        self.description = None
        self.field_id = field_id
        self.annotations = []

    def sdk(self):
        """
        An instance of the ZDAISDK that was passed through the CustomFieldTrainer constructor
        Returns as a method
        """
        return self._sdk

    def create_empty(self):
        """
        Creates a new custom field
        """
        field_id, _ = self.sdk().fields.create(field_name = self.name)
        self.field_id = field_id

    def create_from_field(self, field_id):
        """
        Creates a new custom field using another field as its base
        """
        field_id, _ = self.sdk().fields.create(field_name = self.name,
                                        from_field_id = field_id)
        self.field_id = field_id

    def add_annotation(self, file_id: str, start: int, end: int):
        """
        Add a start and end character range that belongs to a file_id.
        This range will be used during training.
        """
        def add(file_id: str, start: int, end: int):
            self.annotations.append({
                "file_id": file_id,
                "locations": [
                    {
                        "start": start,
                        "end": end
                    }
                ]
            })

        add(file_id, start, end)

    def train(self):
        """
        Creates a new training request using the annotations
        """
        json_annotation = json.dumps(self.annotations)
        request, _ = self.sdk().fields.train(field_id = self.field_id, annotations = json_annotation)

        while True:
            latest = request.update()
            print(f'{latest.get("request_id")} is {latest.get("status")}')

            if request.is_finished():
                break

            time.sleep(2)

    def get_accuracy(self):
        """
        Get the field's accuracy
        """
        accuracy, _ = self.sdk().fields.get_accuracy(field_id = self.field_id)
        return accuracy

    def get_validation_details(self):
        """
        Get the custom field's validation details
        """
        validation_details, _ = self.sdk().fields.get_validation_details(field_id = self.field_id)
        return validation_details

    def get_metadata(self):
        """
        Get the custom field's metadata
        """
        metadata, _ = self.sdk().fields.get_metadata(field_id = self.field_id)
        return metadata
