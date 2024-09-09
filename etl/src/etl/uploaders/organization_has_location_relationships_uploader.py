from typing import Dict, List

from etl.loaders.organizations_loader import OrganizationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class OrganizationHasLocationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Organization",
            "Location",
            "ORGANIZATION_HAS_LOCATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        organizations = OrganizationsLoader().load_saved_items()
        pairs = []
        for organization in organizations:
            if organization.location is None:
                continue
            pair = {
                "start_id": organization.id,
                "end_id": organization.location.id,
            }
            pairs.append(pair)
        return pairs
