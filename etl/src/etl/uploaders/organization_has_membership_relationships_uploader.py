from typing import Dict, List

from etl.loaders.memberships_loader import MembershipsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class OrganizationHasMembershipRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Organization",
            "Membership",
            "ORGANIZATION_HAS_MEMBERSHIP",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        memberships = MembershipsLoader().load_saved_items()
        pairs = []
        for membership in memberships:
            if membership.organization is None:
                continue
            pair = {
                "start_id": membership.organization,
                "end_id": membership.id,
            }
            pairs.append(pair)
        return pairs
