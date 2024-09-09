from typing import Dict, List

from etl.loaders.memberships_loader import MembershipsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PersonHasMembershipRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Person",
            "Membership",
            "PERSON_HAS_MEMBERSHIP",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        memberships = MembershipsLoader().load_saved_items()
        pairs = []
        for x_membership in memberships:
            if x_membership.person is None:
                continue
            pair = {"start_id": x_membership.person, "end_id": x_membership.id}
            pairs.append(pair)
        return pairs
