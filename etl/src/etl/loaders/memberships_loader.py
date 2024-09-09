from typing import List

from etl.models.membership import Membership

from .extractor_base_loader import ExtractorBaseLoader
from .persons_loader import PersonsLoader


class MembershipsLoader(ExtractorBaseLoader[Membership]):
    def __init__(self):
        super().__init__(Membership, "membership", "memberships")

    def _extract_items(self) -> List[Membership]:
        persons = PersonsLoader().load_saved_items()
        memberships = []
        for x_person in persons:
            if not x_person.membership:
                continue
            existing_membership_ids = set()
            for y_membership in memberships:
                existing_membership_ids.add(y_membership.id)
            memberships.extend(
                filter(
                    lambda y_membership: y_membership.id not in existing_membership_ids,
                    x_person.membership,
                )
            )
        return memberships
