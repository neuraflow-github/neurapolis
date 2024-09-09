from abc import ABC, abstractmethod
from typing import Dict, TypeVar

T = TypeVar("T", bound="RisApiDto")


class RisApiDto(ABC):
    @staticmethod
    @abstractmethod
    def from_ris_api_dto(ris_api_dto: Dict) -> T:
        pass
