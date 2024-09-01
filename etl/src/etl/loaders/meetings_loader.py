from etl.models.meeting import Meeting

from .bodies_loader import BodiesLoader
from .paginator_base_loader import PaginatorBaseLoader


class MeetingsLoader(PaginatorBaseLoader[Meeting]):
    def __init__(self):
        super().__init__(
            Meeting,
            "meeting",
            "meetings",
            BodiesLoader().load_saved_items()[0].meeting,
        )
