from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasOriginatorOrganizationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "Organization",
            "PAPER_HAS_ORIGINATOR_ORGANIZATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.originator_organization is None:
                continue
            for y_originator_organization_id in x_paper.originator_organization:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_originator_organization_id,
                }
                pairs.append(pair)
        return pairs
