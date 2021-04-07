from .basemodel import BaseModel


class Classification(BaseModel):
    def __init__(self, json):
        super().__init__(json)

    @property
    def file_id(self) -> str:
        return self.json().get('file_id')

    @property
    def status(self) -> str:
        return self.json().get('status')

    @property
    def request_id(self) -> str:
        return self.json().get('request_id')

    @property
    def classification(self) -> str:
        return self.json().get('classification')

    @property
    def is_contract(self) -> bool:
        is_contract = self.json().get('is_contract')

        if is_contract:
            if isinstance(is_contract, bool):
                return bool(is_contract)
            else:
                raise Exception(f'Unexpected non-boolean is_contract: {is_contract}')
