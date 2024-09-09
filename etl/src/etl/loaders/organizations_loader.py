from etl.models.organization import Organization

from .bodies_loader import BodiesLoader
from .paginator_base_loader import PaginatorBaseLoader


class OrganizationsLoader(PaginatorBaseLoader[Organization]):
    def __init__(self):
        super().__init__(
            Organization,
            "organization",
            "organizations",
            BodiesLoader().load_saved_items()[0].organization,
        )
