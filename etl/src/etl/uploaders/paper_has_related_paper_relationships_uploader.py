from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasRelatedPaperRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Paper",
            "PAPER_RELATED_TO_PAPER",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.related_paper is None:
                continue
            for y_related_paper_id in x_paper.related_paper:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_related_paper_id,
                }
                pairs.append(pair)
        return pairs
