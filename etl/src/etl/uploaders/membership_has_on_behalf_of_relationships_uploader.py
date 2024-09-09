from typing import Dict, List

from etl.loaders.memberships_loader import MembershipsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class MembershipHasOnBehalfOfRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Membership",
            "Organization",
            "MEMBERSHIP_HAS_ON_BEHALF_OF_ORGANIZATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        memberships = MembershipsLoader().load_saved_items()
        pairs = []
        for membership in memberships:
            if membership.on_behalf_of is None:
                continue
            pair = {
                "start_id": membership.id,
                "end_id": membership.on_behalf_of,
            }
            pairs.append(pair)
        return pairs
