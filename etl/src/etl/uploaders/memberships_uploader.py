from typing import List

from etl.loaders.memberships_loader import MembershipsLoader
from etl.models.membership import Membership

from .nodes_base_uploader import NodesBaseUploader


class MembershipsUploader(NodesBaseUploader[Membership]):
    def __init__(self):
        super().__init__(Membership, "Membership")

    def _load_items(self) -> List[Membership]:
        return MembershipsLoader().load_saved_items()
