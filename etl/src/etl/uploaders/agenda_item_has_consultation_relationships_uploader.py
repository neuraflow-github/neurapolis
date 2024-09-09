from typing import Dict, List

from etl.loaders.agenda_items_loader import AgendaItemsLoader
from etl.loaders.consultations_loader import ConsultationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class AgendaItemHasConsultationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "AgendaItem",
            "Consultation",
            "AGENDA_ITEM_HAS_CONSULTATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        agenda_items = AgendaItemsLoader().load_saved_items()
        consultations = ConsultationsLoader().load_saved_items()
        pairs = []
        for x_agenda_item in agenda_items:
            for y_consultation in consultations:
                if y_consultation.agenda_item != x_agenda_item.id:
                    continue
                pair = {
                    "start_id": x_agenda_item.id,
                    "end_id": y_consultation.id,
                }
                pairs.append(pair)
        return pairs
