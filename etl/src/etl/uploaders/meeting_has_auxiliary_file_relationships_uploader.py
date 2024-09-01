from typing import Dict, List

from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class MeetingHasAuxiliaryFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Meeting",
            "File",
            "MEETING_HAS_AUXILIARY_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            if x_meeting.auxiliary_file is None:
                continue
            for y_auxiliary_file in x_meeting.auxiliary_file:
                pair = {"start_id": x_meeting.id, "end_id": y_auxiliary_file.id}
                pairs.append(pair)
        return pairs
