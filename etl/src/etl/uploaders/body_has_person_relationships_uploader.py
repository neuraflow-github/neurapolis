from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.persons_loader import PersonsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasPersonRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "Person",
            "BODY_HAS_PERSON",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        persons = PersonsLoader().load_saved_items()
        pairs = []
        for x_person in persons:
            pair = {
                "start_id": body.id,
                "end_id": x_person.id,
            }
            pairs.append(pair)
        return pairs
