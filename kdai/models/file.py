from .basemodel import BaseModel
from datetime import datetime


class File(BaseModel):
    def __init__(self, json):
        super().__init__(json)
        self._external_id = None

    @property
    def external_id(self):
        return self._external_id

    @external_id.setter
    def external_id(self, value) -> None:
        self._external_id = value

    @property
    def id(self) -> str:
        return self.json().get('file_id')

    @property
    def attributes(self) -> dict:
        return dict(self.json().get('attributes'))

    @property
    def permissions(self) -> list:
        return list(self.json().get('permissions'))

    @property
    def expiration(self) -> datetime:
        dt = self.json().get('expiration')

        if self.json().get('expiration'):
            dt = datetime.strptime(dt, '%Y-%m-%dT%H:%M:%SZ')

        return dt

    def is_kira_ocr(self):
        return True if self.attributes.get('content-type') == 'application/kiraocr' else False
