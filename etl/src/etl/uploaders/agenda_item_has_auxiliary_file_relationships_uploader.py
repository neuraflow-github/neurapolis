from typing import Dict, List

from etl.loaders.agenda_items_loader import AgendaItemsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class AgendaItemHasAuxiliaryFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "AgendaItem",
            "File",
            "AGENDA_ITEM_HAS_AUXILIARY_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        agenda_items = AgendaItemsLoader().load_saved_items()
        pairs = []
        for x_agenda_item in agenda_items:
            if x_agenda_item.auxiliary_file is None:
                continue
            for y_auxiliary_file in x_agenda_item.auxiliary_file:
                pair = {
                    "start_id": x_agenda_item.id,
                    "end_id": y_auxiliary_file.id,
                }
                pairs.append(pair)
        return pairs
