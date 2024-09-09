from typing import List

from etl.models.file import File

from .agenda_items_loader import AgendaItemsLoader
from .extractor_base_loader import ExtractorBaseLoader
from .meetings_loader import MeetingsLoader
from .papers_loader import PapersLoader


class FilesLoader(ExtractorBaseLoader[File]):
    def __init__(self):
        super().__init__(File, "file", "files")

    def _extract_items(self) -> List[File]:
        meetings = MeetingsLoader().load_saved_items()
        agenda_items = AgendaItemsLoader().load_saved_items()
        papers = PapersLoader().load_saved_items()
        files = []
        for x_meeting in meetings:
            if x_meeting.invitation:
                files.append(x_meeting.invitation)
            if x_meeting.results_protocol:
                files.append(x_meeting.results_protocol)
            if x_meeting.verbatim_protocol:
                files.append(x_meeting.verbatim_protocol)
            if x_meeting.auxiliary_file:
                files.extend(x_meeting.auxiliary_file)
        for x_agenda_item in agenda_items:
            if x_agenda_item.auxiliary_file:
                files.extend(x_agenda_item.auxiliary_file)
        for x_paper in papers:
            if x_paper.main_file:
                files.append(x_paper.main_file)
            if x_paper.auxiliary_file:
                files.extend(x_paper.auxiliary_file)
        return files
