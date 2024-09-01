from abc import ABC, abstractmethod


class BaseUploader(ABC):
    @abstractmethod
    def upload_items(self):
        pass
