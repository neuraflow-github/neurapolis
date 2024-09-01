from etl.models.paper import Paper

from .bodies_loader import BodiesLoader
from .paginator_base_loader import PaginatorBaseLoader


class PapersLoader(PaginatorBaseLoader[Paper]):
    def __init__(self):
        super().__init__(
            Paper, "paper", "papers", BodiesLoader().load_saved_items()[0].paper
        )
