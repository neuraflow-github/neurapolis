from typing import List

from etl.loaders.legislative_terms_loader import LegislativeTermsLoader
from etl.models.legislative_term import LegislativeTerm

from .nodes_base_uploader import NodesBaseUploader


class LegislativeTermsUploader(NodesBaseUploader[LegislativeTerm]):
    def __init__(self):
        super().__init__(LegislativeTerm, "LegislativeTerm")

    def _load_items(self) -> List[LegislativeTerm]:
        return LegislativeTermsLoader().load_saved_items()
