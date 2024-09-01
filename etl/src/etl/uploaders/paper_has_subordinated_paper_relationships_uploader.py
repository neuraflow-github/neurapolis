from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasSubordinatedPaperRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Paper",
            "PAPER_HAS_SUBORDINATED_PAPER",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.subordinated_paper is None:
                continue
            for y_subordinated_paper_id in x_paper.subordinated_paper:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_subordinated_paper_id,
                }
                pairs.append(pair)
        return pairs
