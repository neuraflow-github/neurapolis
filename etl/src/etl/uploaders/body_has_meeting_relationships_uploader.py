from typing import Dict, List

from etl.loaders.bodies_loader import BodiesLoader
from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class BodyHasMeetingRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Body",
            "Meeting",
            "BODY_HAS_MEETING",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        body = BodiesLoader().load_saved_items()[0]
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            pair = {
                "start_id": body.id,
                "end_id": x_meeting.id,
            }
            pairs.append(pair)
        return pairs
