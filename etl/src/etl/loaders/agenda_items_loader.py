from typing import List

from etl.models.agenda_item import AgendaItem

from .extractor_base_loader import ExtractorBaseLoader
from .meetings_loader import MeetingsLoader


class AgendaItemsLoader(ExtractorBaseLoader[AgendaItem]):
    def __init__(self):
        super().__init__(AgendaItem, "agenda_item", "agenda_items")

    def _extract_items(self) -> List[AgendaItem]:
        meetings = MeetingsLoader().load_saved_items()
        agenda_items = []
        for x_meeting in meetings:
            if x_meeting.agenda_item is None:
                continue
            for y_agenda_item in x_meeting.agenda_item:
                if y_agenda_item.id in [
                    z_existing_agenda_item.id for z_existing_agenda_item in agenda_items
                ]:
                    continue
                agenda_items.append(y_agenda_item)
        return agenda_items
