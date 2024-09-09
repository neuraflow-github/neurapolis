from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasConsultationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Consultation",
            "PAPER_HAS_CONSULTATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.consultation is None:
                continue
            for y_consultation in x_paper.consultation:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_consultation.id,
                }
                pairs.append(pair)
        return pairs
