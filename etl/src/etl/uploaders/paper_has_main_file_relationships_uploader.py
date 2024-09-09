from typing import Dict, List

from etl.loaders.papers_loader import PapersLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class PaperHasMainFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Paper",
            "File",
            "PAPER_HAS_MAIN_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        papers = PapersLoader().load_saved_items()
        pairs = []
        for paper in papers:
            if paper.main_file is None:
                continue
            pair = {
                "start_id": paper.id,
                "end_id": paper.main_file.id,
            }
            pairs.append(pair)
        return pairs
