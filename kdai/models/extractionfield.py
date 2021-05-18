from .basemodel import BaseModel
from .extractionresult import ExtractionResult


class ExtractionField(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def field_id(self):
        return self.json().get('field_id', None)

    @property
    def extractions(self):
        extractions = self.json().get('extractions', None)
        _e = []
        if extractions:
            for _extraction in extractions:
                _e.append(ExtractionResult(_extraction))

        return _e
