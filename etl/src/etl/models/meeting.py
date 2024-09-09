from typing import Dict, List, Optional

from .agenda_item import AgendaItem
from .db_dict import DbDict
from .file import File
from .location import Location
from .ris_api_dto import RisApiDto


class Meeting(RisApiDto, DbDict):
    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        name: Optional[str],
        meeting_state: Optional[str],
        cancelled: Optional[bool],
        start: Optional[str],
        end: Optional[str],
        location: Optional[Location],
        organization: Optional[List[str]],
        participant: Optional[List[str]],
        invitation: Optional[File],
        results_protocol: Optional[File],
        verbatim_protocol: Optional[File],
        auxiliary_file: Optional[List[File]],
        agenda_item: Optional[List[AgendaItem]],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[str],
        modified: Optional[str],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.name = name
        self.meeting_state = meeting_state
        self.cancelled = cancelled
        self.start = start
        self.end = end
        self.location = location
        self.organization = organization
        self.participant = participant
        self.invitation = invitation
        self.results_protocol = results_protocol
        self.verbatim_protocol = verbatim_protocol
        self.auxiliary_file = auxiliary_file
        self.agenda_item = agenda_item
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(meeting_ris_api_dto: Dict) -> "Meeting":
        return Meeting(
            id=meeting_ris_api_dto.get("id"),
            type=meeting_ris_api_dto.get("type"),
            name=meeting_ris_api_dto.get("name"),
            meeting_state=meeting_ris_api_dto.get("meetingState"),
            cancelled=meeting_ris_api_dto.get("cancelled"),
            start=meeting_ris_api_dto.get("start"),
            end=meeting_ris_api_dto.get("end"),
            location=(
                Location.from_ris_api_dto(meeting_ris_api_dto.get("location"))
                if meeting_ris_api_dto.get("location")
                else None
            ),
            organization=meeting_ris_api_dto.get("organization"),
            participant=meeting_ris_api_dto.get("participant"),
            invitation=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("invitation"))
                if meeting_ris_api_dto.get("invitation")
                else None
            ),
            results_protocol=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("resultsProtocol"))
                if meeting_ris_api_dto.get("resultsProtocol")
                else None
            ),
            verbatim_protocol=(
                File.from_ris_api_dto(meeting_ris_api_dto.get("verbatimProtocol"))
                if meeting_ris_api_dto.get("verbatimProtocol")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_file_ris_api_dto)
                    for x_file_ris_api_dto in meeting_ris_api_dto.get("auxiliaryFile")
                ]
                if meeting_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            agenda_item=(
                [
                    AgendaItem.from_ris_api_dto(x_agenda_item_ris_api_dto)
                    for x_agenda_item_ris_api_dto in meeting_ris_api_dto.get(
                        "agendaItem"
                    )
                ]
                if meeting_ris_api_dto.get("agendaItem")
                else None
            ),
            license=meeting_ris_api_dto.get("license"),
            keyword=meeting_ris_api_dto.get("keyword"),
            created=meeting_ris_api_dto.get("created"),
            modified=meeting_ris_api_dto.get("modified"),
            web=meeting_ris_api_dto.get("web"),
            deleted=meeting_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "meeting_state": self.meeting_state,
            "cancelled": self.cancelled,
            "start": self.start,
            "end": self.end,
            "location": self.location.to_dict() if self.location else None,
            "organization": self.organization,
            "participant": self.participant,
            "invitation": self.invitation.to_dict() if self.invitation else None,
            "results_protocol": (
                self.results_protocol.to_dict() if self.results_protocol else None
            ),
            "verbatim_protocol": (
                self.verbatim_protocol.to_dict() if self.verbatim_protocol else None
            ),
            "auxiliary_file": (
                [x_file.to_dict() for x_file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "agenda_item": (
                [x_agenda_item.to_dict() for x_agenda_item in self.agenda_item]
                if self.agenda_item
                else None
            ),
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_dict_without_nested(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "meeting_state": self.meeting_state,
            "cancelled": self.cancelled,
            "start": self.start,
            "end": self.end,
            "location": self.location.to_dict() if self.location else None,
            "organization": self.organization,
            "participant": self.participant,
            "invitation": self.invitation.id if self.invitation else None,
            "results_protocol": (
                self.results_protocol.id if self.results_protocol else None
            ),
            "verbatim_protocol": (
                self.verbatim_protocol.id if self.verbatim_protocol else None
            ),
            "auxiliary_file": (
                [x_file.id for x_file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "agenda_item": (
                [x_agenda_item.id for x_agenda_item in self.agenda_item]
                if self.agenda_item
                else None
            ),
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_db_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "meeting_state": self.meeting_state,
            "cancelled": self.cancelled,
            "start": self.start,
            "end": self.end,
            # "location": self.location,
            # "organization": self.organization,
            # "participant": self.participant,
            # "invitation": self.invitation,
            # "results_protocol": self.results_protocol,
            # "verbatim_protocol": self.verbatim_protocol,
            # "auxiliary_file": self.auxiliary_file,
            # "agenda_item": self.agenda_item,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
