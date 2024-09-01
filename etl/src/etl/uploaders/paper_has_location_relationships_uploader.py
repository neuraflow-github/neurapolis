from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasLocationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Location",
            "PAPER_HAS_LOCATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.location is None:
                continue
            for y_location in x_paper.location:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_location.id,
                }
                pairs.append(pair)
        return pairs
