from etl.models.person import Person

from .bodies_loader import BodiesLoader
from .paginator_base_loader import PaginatorBaseLoader


class PersonsLoader(PaginatorBaseLoader[Person]):
    def __init__(self):
        super().__init__(
            Person,
            "person",
            "persons",
            BodiesLoader().load_saved_items()[0].person,
        )
