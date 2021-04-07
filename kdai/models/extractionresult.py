from .basemodel import BaseModel


class ExtractionResult(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def text(self):
        return self.json().get('text')

    @property
    def spans(self):
        return self.json().get('spans')
