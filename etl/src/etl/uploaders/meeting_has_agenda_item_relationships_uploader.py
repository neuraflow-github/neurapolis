from typing import Dict, List

from etl.loaders.meetings_loader import MeetingsLoader

from .relationships_base_uploader import RelationshipsBaseUploader


class MeetingHasAgendaItemRelationshipsUploader(RelationshipsBaseUploader):
    def __init__(self):
        super().__init__(
            "Meeting",
            "AgendaItem",
            "MEETING_HAS_AGENDA_ITEM",
        )

    def _get_pairs(self) -> List[Dict[str, str]]:
        meetings = MeetingsLoader().load_saved_items()
        pairs = []
        for x_meeting in meetings:
            if x_meeting.agenda_item is None:
                continue
            for y_agenda_item in x_meeting.agenda_item:
                pair = {"start_id": x_meeting.id, "end_id": y_agenda_item.id}
                pairs.append(pair)
        return pairs
