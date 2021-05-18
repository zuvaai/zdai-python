class BaseModel(object):
    """
    BaseModel contains the base methods of the KDAI model
    """
    def __init__(self, json: dict):
        self._data = json

    def __repr__(self) -> str:
        _data = ', '.join("{}={!r}".format(k, v) for k, v in vars(self).get('_data').items())
        return f'{self.__class__.__name__}({_data})'

    def json(self) -> dict:
        """
        Returns the json data of the model
        """
        return self._data

    def is_done(self) -> bool:
        """
        If the model contains a status, returns if the model has completed or not
        """
        if not self._data.get('status'):
            pass

        return self._data.get('status') in ['failed', 'complete']

    def is_successful(self) -> bool:
        """
        Returns whether the status is set to 'complete' (i.e. a request that completed successfully).
        """
        return self._data.get('status') == 'complete'
