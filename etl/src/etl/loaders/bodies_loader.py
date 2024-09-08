from typing import List

from etl.config import config
from etl.models.body import Body

from .base_loader import BaseLoader


class BodiesLoader(BaseLoader[Body]):
    def __init__(self):
        super().__init__(Body, "body", "bodies")

    def _load_items(self, existing_items: List[Body]) -> List[Body]:
        print("TEST")
        print(config.api_url)
        body = Body.from_ris_api_dto({"id": config.api_url})
        print(Body.from_ris_api_dto({"id": config.api_url}))
        print(body.id)
        body = self._fetch_detailed_item(
            existing_items, Body.from_ris_api_dto({"id": config.api_url})
        )
        return [body]
