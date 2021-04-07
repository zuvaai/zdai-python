from .basemodel import BaseModel
from .extractionfield import ExtractionField


class Extraction(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def file_id(self):
        return self.json().get('file_id')

    @property
    def request_id(self):
        return self.json().get('request_id')

    @property
    def requested_field_ids(self):
        return self.json().get('field_ids')

    @property
    def status(self):
        return self.json().get('status')

    @property
    def fields(self):
        results = self.json().get('results')
        _r = []
        if results:
            for result in results:
                _r.append(ExtractionField(result))
        return _r
