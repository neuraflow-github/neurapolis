from typing import Dict, List

from etl.loaders.consultations_loader import ConsultationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class OrganizationHasConsultationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Organization",
            "Consultation",
            "ORGANIZATION_HAS_CONSULTATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        consultations = ConsultationsLoader().load_saved_items()
        pairs = []
        for x_consultation in consultations:
            if x_consultation.organization is None:
                continue
            for y_organization_id in x_consultation.organization:
                pair = {
                    "start_id": y_organization_id,
                    "end_id": x_consultation.id,
                }
                pairs.append(pair)
        return pairs
