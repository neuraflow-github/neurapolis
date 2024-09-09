from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasAuxiliaryFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "File",
            "PAPER_HAS_AUXILIARY_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for x_paper in papers:
            if x_paper.auxiliary_file is None:
                continue
            for y_auxiliary_file in x_paper.auxiliary_file:
                pair = {
                    "start_id": x_paper.id,
                    "end_id": y_auxiliary_file.id,
                }
                pairs.append(pair)
        return pairs
