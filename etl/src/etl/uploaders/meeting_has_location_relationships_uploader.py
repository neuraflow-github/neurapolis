from typing import Dict, List

from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class MeetingHasLocationRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Meeting",
            "Location",
            "MEETING_HAS_LOCATION",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            if x_meeting.location is None:
                continue
            pair = {
                "start_id": x_meeting.id,
                "end_id": x_meeting.location.id,
            }
            pairs.append(pair)
        return pairs
