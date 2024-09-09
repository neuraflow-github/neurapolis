from typing import List

from etl.loaders.bodies_loader import BodiesLoader
from etl.models.body import Body

from .nodes_base_uploader import NodesBaseUploader


class BodyUploader(NodesBaseUploader[Body]):
    def __init__(self):
        super().__init__(Body, "Body")

    def _load_items(self) -> List[Body]:
        return BodiesLoader().load_saved_items()
