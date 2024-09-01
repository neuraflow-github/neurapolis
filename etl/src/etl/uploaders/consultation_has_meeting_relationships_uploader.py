from typing import Dict, List

from etl.loaders.consultations_loader import ConsultationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class ConsultationHasMeetingRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Consultation",
            "Meeting",
            "CONSULTATION_HAS_MEETING",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        consultations = ConsultationsLoader().load_saved_items()
        pairs = []
        for x_consultation in consultations:
            if x_consultation.meeting is None:
                continue
            pair = {
                "start_id": x_consultation.id,
                "end_id": x_consultation.meeting,
            }
            pairs.append(pair)
        return pairs
