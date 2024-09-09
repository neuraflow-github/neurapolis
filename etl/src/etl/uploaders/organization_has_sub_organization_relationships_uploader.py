from typing import Dict, List

from etl.loaders.organizations_loader import OrganizationsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class OrganizationHasSubOrganizationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Organization",
            "Organization",
            "ORGANIZATION_HAS_SUB_ORGANIZATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        organizations = OrganizationsLoader().load_saved_items()
        pairs = []
        for organization in organizations:
            if organization.sub_organization_of is None:
                continue
            pair = {
                "start_id": organization.sub_organization_of,
                "end_id": organization.id,
            }
            pairs.append(pair)
        return pairs
