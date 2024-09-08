import json
import logging
import os
import pickle
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Generic, List, Type, TypeVar

import requests

from etl.config import config
from etl.models.ris_api_dto import RisApiDto
from etl.utilities.request_session import request_session

T = TypeVar("T", bound=RisApiDto)


class BaseLoader(ABC, Generic[T]):
    def __init__(self, item_class: Type[T], item_name: str, plural_item_name: str):
        self._item_class = item_class
        self._item_name = item_name
        self._plural_item_name = plural_item_name
        self._start_time = None

    def _fetch_detailed_item(self, existing_items: T, item: T) -> T | None:
        if item.deleted:
            logging.info(
                f"{self.__class__.__name__}: Skipping loading detailed {self._item_name}: {item.id}: Item is deleted"
            )
            return None
        existing_item = None
        for x_existing_item in existing_items:
            if x_existing_item.id == item.id:
                existing_item = x_existing_item
                break
        if (
            existing_item
            and item.modified is not None
            and existing_item.modified is not None
            and datetime.fromisoformat(item.modified)
            <= datetime.fromisoformat(existing_item.modified)
        ):
            logging.info(
                f"{self.__class__.__name__}: Skipping loading detailed {self._item_name}: {item.id}: Item is not modified"
            )
            return existing_item
        try:
            response = request_session.get(item.id)
            if 400 <= response.status_code < 500:
                logging.info(
                    f"{self.__class__.__name__}: Ignoring detailed {self._item_name}: {item.id}: Statuscode {response.status_code}"
                )
                return None
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(
                f"{self.__class__.__name__}: Failed to load detailed {self._item_name}: {item.id}: {e}"
            )
            return None
        item_ris_api_dto = response.json()
        item = self._item_class.from_ris_api_dto(item_ris_api_dto)
        if item.deleted:
            logging.info(
                f"{self.__class__.__name__}: Ignoring detailed {self._item_name}: {item.id}: Item is deleted"
            )
            return None
        return item

    def _load_detailed_items(self, existing_items: List[T], items: List[T]) -> List[T]:
        detailed_items = []
        item_count = len(items)
        processed_item_count = 0
        logging.info(
            f"{self.__class__.__name__}: Started loading {item_count} detailed {self._plural_item_name}..."
        )
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_detailed_item = {}
            for x_item in items:
                future = executor.submit(
                    self._fetch_detailed_item, existing_items, x_item
                )
                future_to_detailed_item[future] = x_item
            for x_future in as_completed(future_to_detailed_item):
                detailed_item = x_future.result()
                if detailed_item is not None:
                    detailed_items.append(detailed_item)
                processed_item_count += 1
                if processed_item_count % 10 == 0 or processed_item_count == item_count:
                    logging.info(
                        f"{self.__class__.__name__}: Loaded {processed_item_count}/{item_count} ({processed_item_count/item_count*100:.2f}%) {self._plural_item_name}"
                    )
        logging.info(
            f"{self.__class__.__name__}: Finished loading {len(detailed_items)} detailed {self._plural_item_name}"
        )
        return detailed_items

    @abstractmethod
    def _load_items(self, existing_items: List[T]) -> List[T]:
        pass

    def _wrapped_load_items(self) -> List[T]:
        logging.info(
            f"{self.__class__.__name__}: Started loading {self._plural_item_name}..."
        )
        existing_items = self.load_saved_items()
        items = self._load_items(existing_items)
        logging.info(
            f"{self.__class__.__name__}: Finished loading {len(items)} {self._plural_item_name}"
        )
        return items

    def load_and_save_items(self):
        self._start_time = time.time()
        logging.info(
            f"{self.__class__.__name__}: Started loading and saving {self._plural_item_name}..."
        )
        items = self._wrapped_load_items()
        item_count = len(items)
        logging.info(
            f"{self.__class__.__name__}: Started saving {item_count} {self._plural_item_name}..."
        )
        items_pickle_file_path = os.path.join(
            config.data_dir_path, f"{self._plural_item_name}.pickle"
        )
        with open(items_pickle_file_path, "wb") as items_pickle_file:
            pickle.dump(items, items_pickle_file)
        test_items_json_file_path = os.path.join(
            config.data_dir_path, f"test_{self._plural_item_name}.json"
        )
        test_item_db_dicts = []
        for x_item in items[:: max(1, len(items) // 100)][:100]:
            test_item_db_dict = x_item.to_db_dict()
            test_item_db_dicts.append(test_item_db_dict)
        with open(test_items_json_file_path, "w") as test_items_json_file:
            json.dump(
                test_item_db_dicts, test_items_json_file, indent=4, ensure_ascii=False
            )
        elapsed_time = time.time() - self._start_time
        logging.info(
            f"{self.__class__.__name__}: Finished loading and saving {item_count} {self._plural_item_name} in {elapsed_time:.2f} seconds"
        )

    def load_saved_items(self) -> List[T]:
        items_pickle_file_path = os.path.join(
            config.data_dir_path, f"{self._plural_item_name}.pickle"
        )
        if not os.path.exists(items_pickle_file_path):
            logging.info(
                f"{self.__class__.__name__}: Not found file: {items_pickle_file_path}"
            )
            return []
        with open(items_pickle_file_path, "rb") as items_pickle_file:
            items: List[T] = pickle.load(items_pickle_file)
            return items
