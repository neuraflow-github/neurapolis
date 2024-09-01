import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Type, TypeVar

import requests

from etl.utilities.config import config
from etl.utilities.request_session import request_session

from .base_loader import BaseLoader

T = TypeVar("T")


class PaginatorBaseLoader(BaseLoader[T]):
    def __init__(
        self,
        item_class: Type[T],
        item_name: str,
        plural_item_name: str,
        endpoint: str,
    ):
        super().__init__(item_class, item_name, plural_item_name)
        self._item_class = item_class
        self._endpoint = endpoint

    def _fetch_page(self, url: str) -> dict | None:
        try:
            response = request_session.get(url)
            if 400 <= response.status_code < 500:
                logging.info(
                    f"{self.__class__.__name__}: Ignoring page {url}: Statuscode {response.status_code}"
                )
                return None
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"{self.__class__.__name__}: Failed to fetch page {url}: {e}")
            return None

    def _load_basic_items(self) -> List[T]:
        logging.info(
            f"{self.__class__.__name__}: Started loading basic {self._plural_item_name}..."
        )
        basic_items = []
        fist_page_url = f"{config.api_url}/{self._endpoint}"
        first_page_response = request_session.get(fist_page_url)
        first_page_response.raise_for_status()
        first_page_response_data = first_page_response.json()
        total_elements = first_page_response_data["pagination"]["totalElements"]
        page_size = len(first_page_response_data["data"])
        total_pages = (total_elements + page_size - 1) // page_size
        page_urls = []
        for x_page_number in range(1, total_pages + 1):
            page_urls.append(f"{config.api_url}/{self._endpoint}/page/{x_page_number}")
        with ThreadPoolExecutor(max_workers=8) as executor:
            url_to_future_map = {}
            for x_page_url in page_urls:
                future = executor.submit(self._fetch_page, x_page_url)
                url_to_future_map[x_page_url] = future
            for x_url in as_completed(url_to_future_map):
                future_response_data = url_to_future_map[x_url].result()
                if future_response_data is None:
                    continue
                for x_item_ris_api_dto in future_response_data["data"]:
                    basic_item = self._item_class.from_ris_api_dto(x_item_ris_api_dto)
                    basic_items.append(basic_item)
                    logging.info(
                        f"{self.__class__.__name__}: Loaded {len(basic_items)}/{total_elements} ({len(basic_items)/total_elements*100:.2f}%) basic {self._plural_item_name}"
                    )
        logging.info(
            f"{self.__class__.__name__}: Finished loading {len(basic_items)} basic {self._plural_item_name}"
        )
        return basic_items

    def _load_items(self, existing_items: List[T]) -> List[T]:
        basic_items = self._load_basic_items()
        return self._load_detailed_items(existing_items, basic_items)
