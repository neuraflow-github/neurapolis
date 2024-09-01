from abc import ABC, abstractmethod


class DbDict(ABC):
    @abstractmethod
    def to_db_dict(self) -> dict:
        pass
