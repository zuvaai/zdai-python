import kdai as kdai
from .api.exceptions import ApiNoAccessProvidedError


class KDAISDK(object):
    """
    Kira Document AI (KDAI) SDK which acts as an entry-point to get an instance of
    an API class that's associated to a KDAI microservice.
    """

    def __init__(self, url: str = None, token: str = None, from_config=False):
        self.url = url
        self.token = token

        if from_config:
            self.url, self.token = kdai.config.get_access()

        if not self.has_access():
            raise ApiNoAccessProvidedError(url = self.url, token = self.token)

        self._load_apis()

    def _load_apis(self):
        self._file_api = kdai.FileAPI(url = self.url, token = self.token)
        self._classification_api = kdai.ClassificationAPI(url = self.url, token = self.token)
        self._language_api = kdai.LanguageAPI(url = self.url, token = self.token)
        self._extraction_api = kdai.ExtractionAPI(url = self.url, token = self.token)
        self._field_api = kdai.FieldAPI(url = self.url, token = self.token)
        self._ocr_api = kdai.OCRAPI(url = self.url, token = self.token)

    def has_access(self):
        return all(f is not None for f in [self.url, self.token])

    @property
    def file(self) -> kdai.FileAPI:
        """
        Returns the FileAPI instance
        """
        return self._file_api

    @property
    def classification(self) -> kdai.ClassificationAPI:
        """
        Returns the ClassificationAPI instance
        """
        return self._classification_api

    @property
    def language(self) -> kdai.LanguageAPI:
        """
        Returns the LanguageAPI instance
        """
        return self._language_api

    @property
    def extraction(self) -> kdai.ExtractionAPI:
        """
        Returns the ExtractionAPI instance
        """
        return self._extraction_api

    @property
    def fields(self) -> kdai.FieldAPI:
        """
        Returns the FieldAPI instance
        """
        return self._field_api

    @property
    def ocr(self) -> kdai.OCRAPI:
        """
        Returns the OCRAPI instance
        """
        return self._ocr_api

    @property
    def config(self):
        """
        Returns the config
        """
        return kdai.config
