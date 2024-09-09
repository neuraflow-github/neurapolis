from typing import Dict, List

from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class OrganizationHasMeetingRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Organization",
            "Meeting",
            "ORGANIZATION_HAS_MEETING",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            if x_meeting.organization is None:
                continue
            for y_organization_id in x_meeting.organization:
                pair = {
                    "start_id": y_organization_id,
                    "end_id": x_meeting.id,
                }
                pairs.append(pair)
        return pairs
