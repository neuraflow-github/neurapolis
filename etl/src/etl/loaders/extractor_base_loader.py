import logging
from abc import abstractmethod
from typing import List, Type, TypeVar

from .base_loader import BaseLoader

T = TypeVar("T")


class ExtractorBaseLoader(BaseLoader[T]):
    def __init__(self, item_class: Type[T], item_name: str, plural_item_name: str):
        super().__init__(item_class, item_name, plural_item_name)

    @abstractmethod
    def _extract_items(self) -> List[T]:
        pass

    def _wrapping_extract_items(self) -> List[T]:
        logging.info(
            f"{self.__class__.__name__}: Started extracting {self._plural_item_name}..."
        )
        items = self._extract_items()
        unique_items_dict = {}
        for x_item in items:
            unique_items_dict[x_item.id] = x_item
        unique_items = list(unique_items_dict.values())
        logging.info(
            f"{self.__class__.__name__}: Finished extracting {len(items)} {self._plural_item_name} and {len(unique_items)} unique {self._plural_item_name}"
        )
        return unique_items

    def _load_items(self, existing_items: List[T]) -> List[T]:
        basic_items = self._extract_items()
        return self._load_detailed_items(existing_items, basic_items)
