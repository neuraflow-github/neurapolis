from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasPaperRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "Paper",
            "BODY_HAS_PAPER",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            pair = {
                "start_id": body.id,
                "end_id": x_paper.id,
            }
            pairs.append(pair)
        return pairs
