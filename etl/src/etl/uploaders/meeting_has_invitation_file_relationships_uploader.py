from typing import Dict, List

from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class MeetingHasInvitationFileRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Meeting",
            "File",
            "MEETING_HAS_INVITATION_FILE",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            if x_meeting.invitation is None:
                continue
            pair = {
                "start_id": x_meeting.id,
                "end_id": x_meeting.invitation.id,
            }
            pairs.append(pair)
        return pairs
