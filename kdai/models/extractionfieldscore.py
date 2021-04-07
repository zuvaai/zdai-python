from .basemodel import BaseModel


class ExtractionFieldScore(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def score_class(self):
        return self.json().get('class', None)

    @property
    def score(self):
        return self.json().get('score', None)

    @property
    def label(self):
        return self.json().get('label', None)
