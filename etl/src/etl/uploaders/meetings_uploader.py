from typing import List

from etl.loaders.meetings_loader import MeetingsLoader
from etl.models.meeting import Meeting

from .nodes_base_uploader import NodesBaseUploader


class MeetingsUploader(NodesBaseUploader[Meeting]):
    def __init__(self):
        super().__init__(Meeting, "Meeting")

    def _load_items(self) -> List[Meeting]:
        return MeetingsLoader().load_saved_items()
