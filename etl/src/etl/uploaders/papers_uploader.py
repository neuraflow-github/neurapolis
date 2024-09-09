from typing import List

from etl.loaders.papers_loader import PapersLoader
from etl.models.paper import Paper

from .nodes_base_uploader import NodesBaseUploader


class PapersUploader(NodesBaseUploader):
    def __init__(self):
        super().__init__(Paper, "Paper")

    def _load_items(self) -> List[Paper]:
        return PapersLoader().load_saved_items()
