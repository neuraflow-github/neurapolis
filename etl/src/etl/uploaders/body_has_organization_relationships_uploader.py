from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.organizations_loader import OrganizationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasOrganizationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "Organization",
            "BODY_HAS_ORGANIZATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        organizations = OrganizationsLoader().load_saved_items()
        pairs = []
        for organization in organizations:
            pair = {
                "start_id": body.id,
                "end_id": organization.id,
            }
            pairs.append(pair)
        return pairs
