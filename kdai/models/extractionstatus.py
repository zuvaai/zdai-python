from .basemodel import BaseModel


class ExtractionStatus(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def request_id(self):
        return self.json().get('request_id')

    @property
    def status(self):
        return self.json().get('status')
