from .basemodel import BaseModel


class Language(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def request_id(self):
        return self.json().get('request_id')

    @property
    def file_id(self):
        return self.json().get('file_id')

    @property
    def status(self):
        return self.json().get('status')

    @property
    def language(self):
        return self.json().get('language')
