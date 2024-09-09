from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class Consultation(RisApiDto, DbDict):
    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        paper: Optional[str],
        agenda_item: Optional[str],
        meeting: Optional[str],
        organization: Optional[List[str]],
        authoritative: Optional[bool],
        role: Optional[str],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.paper = paper
        self.agenda_item = agenda_item
        self.meeting = meeting
        self.organization = organization
        self.authoritative = authoritative
        self.role = role
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(consultation_ris_api_dto: Dict) -> "Consultation":
        return Consultation(
            id=consultation_ris_api_dto.get("id"),
            type=consultation_ris_api_dto.get("type"),
            paper=consultation_ris_api_dto.get("paper"),
            agenda_item=consultation_ris_api_dto.get("agendaItem"),
            meeting=consultation_ris_api_dto.get("meeting"),
            organization=consultation_ris_api_dto.get("organization"),
            authoritative=consultation_ris_api_dto.get("authoritative"),
            role=consultation_ris_api_dto.get("role"),
            license=consultation_ris_api_dto.get("license"),
            keyword=consultation_ris_api_dto.get("keyword"),
            created=consultation_ris_api_dto.get("created"),
            modified=consultation_ris_api_dto.get("modified"),
            web=consultation_ris_api_dto.get("web"),
            deleted=consultation_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "paper": self.paper,
            "agenda_item": self.agenda_item,
            "meeting": self.meeting,
            "organization": self.organization,
            "authoritative": self.authoritative,
            "role": self.role,
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
            # "paper": self.paper,
            # "agenda_item": self.agenda_item,
            # "meeting": self.meeting,
            # "organization": self.organization,
            "authoritative": self.authoritative,
            "role": self.role,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
