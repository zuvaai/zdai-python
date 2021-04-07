from .basemodel import BaseModel
from .extractionresult import ExtractionResult
from .extractionfieldscore import ExtractionFieldScore


class ExtractionField(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def field_id(self):
        return self.json().get('field_id', None)

    @property
    def scores(self):
        scores = self.json().get('scores', None)
        _scores = []
        if scores:
            for score in scores:
                _scores.append(ExtractionFieldScore(score))
        return _scores

    @property
    def extractions(self):
        extractions = self.json().get('extractions', None)
        _e = []
        if extractions:
            for _extraction in extractions:
                _e.append(ExtractionResult(_extraction))

        return _e
