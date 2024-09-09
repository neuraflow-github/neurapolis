from typing import List

from etl.loaders.organizations_loader import OrganizationsLoader
from etl.models.organization import Organization

from .nodes_base_uploader import NodesBaseUploader


class OrganizationsUploader(NodesBaseUploader[Organization]):
    def __init__(self):
        super().__init__(Organization, "Organization")

    def _load_items(self) -> List[Organization]:
        return OrganizationsLoader().load_saved_items()
