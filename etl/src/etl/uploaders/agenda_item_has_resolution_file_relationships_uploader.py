from typing import Dict, List

from etl.loaders.agenda_items_loader import AgendaItemsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class AgendaItemHasResolutionFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "AgendaItem",
            "File",
            "AGENDA_ITEM_HAS_RESOLUTION_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        agenda_items = AgendaItemsLoader().load_saved_items()
        pairs = []
        for agenda_item in agenda_items:
            if agenda_item.resolution_file is None:
                continue
            pair = {
                "start_id": agenda_item.id,
                "end_id": agenda_item.resolution_file.id,
            }
            pairs.append(pair)
        return pairs
