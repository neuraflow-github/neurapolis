from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasSuperordinatedPaperRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Paper",
            "PAPER_SUPERORDINATED_TO_PAPER",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.superordinated_paper is None:
                continue
            for y_superordinated_paper_id in x_paper.superordinated_paper:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_superordinated_paper_id,
                }
                pairs.append(pair)
        return pairs
