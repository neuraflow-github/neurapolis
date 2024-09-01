from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.legislative_terms_loader import LegislativeTermsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasLegislativeTermRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "LegislativeTerm",
            "BODY_HAS_LEGISLATIVE_TERM",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        legislative_terms = LegislativeTermsLoader().load_saved_items()
        pairs = []
        for x_legislative_term in legislative_terms:
            pair = {
                "start_id": body.id,
                "end_id": x_legislative_term.id,
            }
            pairs.append(pair)
        return pairs
