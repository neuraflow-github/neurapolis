from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasLocationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "Location",
            "BODY_HAS_LOCATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        if body.location is None:
            return []
        return [({"start_id": body.id, "end_id": body.location.id})]
