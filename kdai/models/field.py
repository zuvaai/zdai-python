from .basemodel import BaseModel


class Field(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def id(self) -> str:
        return self.json().get('field_id')

    @property
    def name(self) -> str:
        return self.json().get('name')

    @property
    def description(self) -> str:
        return self.json().get('description')

    @property
    def bias(self) -> float:
        return float(self.json().get('bias'))

    @property
    def fscore(self) -> float:
        return float(self.json().get('f_score'))

    @property
    def precision(self) -> float:
        return float(self.json().get('precision'))

    @property
    def recall(self) -> float:
        return float(self.json().get('recall'))

    @property
    def document_count(self) -> int:
        return int(self.json().get('document_count'))

    @property
    def is_custom(self):
        return bool(self.json().get('is_custom'))
