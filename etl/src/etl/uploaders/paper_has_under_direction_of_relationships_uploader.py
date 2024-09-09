from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasUnderDirectionOfRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Organization",
            "PAPER_HAS_UNDER_DIRECTION_OF_ORGANIZATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for paper in papers:
            if paper.under_direction_of is None:
                continue
            for under_direction_of_organization_id in paper.under_direction_of:
                pair = {
                    "start_id": paper.id,
                    "end_id": under_direction_of_organization_id,
                }
                pairs.append(pair)
        return pairs
