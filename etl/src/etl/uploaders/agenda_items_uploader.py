from typing import List

from etl.loaders.agenda_items_loader import AgendaItemsLoader
from etl.models.agenda_item import AgendaItem

from .nodes_base_uploader import NodesBaseUploader


class AgendaItemsUploader(NodesBaseUploader[AgendaItem]):
    def __init__(self):
        super().__init__(AgendaItem, "AgendaItem")

    def _load_items(self) -> List[AgendaItem]:
        return AgendaItemsLoader().load_saved_items()
