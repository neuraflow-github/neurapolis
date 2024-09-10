from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .file import File
from .ris_api_dto import RisApiDto


class AgendaItem(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    meeting: Optional[str]
    number: Optional[str]
    order: Optional[int]
    name: Optional[str]
    public: Optional[bool]
    consultation: Optional[str]
    result: Optional[str]
    resolution_text: Optional[str]
    resolution_file: Optional[File]
    auxiliary_file: Optional[List[File]]
    start: Optional[datetime]
    end: Optional[datetime]
    license: Optional[str]
    keyword: Optional[List[str]]
    created: Optional[datetime]
    modified: Optional[datetime]
    web: Optional[str]
    deleted: Optional[bool]

    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        meeting: Optional[str],
        number: Optional[str],
        order: Optional[int],
        name: Optional[str],
        public: Optional[bool],
        consultation: Optional[str],
        result: Optional[str],
        resolution_text: Optional[str],
        resolution_file: Optional[File],
        auxiliary_file: Optional[List[File]],
        start: Optional[datetime],
        end: Optional[datetime],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.meeting = meeting
        self.number = number
        self.order = order
        self.name = name
        self.public = public
        self.consultation = consultation
        self.result = result
        self.resolution_text = resolution_text
        self.resolution_file = resolution_file
        self.auxiliary_file = auxiliary_file
        self.start = start
        self.end = end
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(agenda_item_ris_api_dto: Dict) -> "AgendaItem":
        return AgendaItem(
            id=agenda_item_ris_api_dto.get("id"),
            type=agenda_item_ris_api_dto.get("type"),
            meeting=agenda_item_ris_api_dto.get("meeting"),
            number=agenda_item_ris_api_dto.get("number"),
            order=agenda_item_ris_api_dto.get("order"),
            name=agenda_item_ris_api_dto.get("name"),
            public=agenda_item_ris_api_dto.get("public"),
            consultation=agenda_item_ris_api_dto.get("consultation"),
            result=agenda_item_ris_api_dto.get("result"),
            resolution_text=agenda_item_ris_api_dto.get("resolutionText"),
            resolution_file=(
                File.from_ris_api_dto(agenda_item_ris_api_dto.get("resolutionFile"))
                if agenda_item_ris_api_dto.get("resolutionFile")
                else None
            ),
            auxiliary_file=(
                [
                    File.from_ris_api_dto(x_auxiliary_file_ris_api_dto)
                    for x_auxiliary_file_ris_api_dto in agenda_item_ris_api_dto.get(
                        "auxiliaryFile"
                    )
                ]
                if agenda_item_ris_api_dto.get("auxiliaryFile")
                else None
            ),
            start=agenda_item_ris_api_dto.get("start"),
            end=agenda_item_ris_api_dto.get("end"),
            license=agenda_item_ris_api_dto.get("license"),
            keyword=agenda_item_ris_api_dto.get("keyword"),
            created=agenda_item_ris_api_dto.get("created"),
            modified=agenda_item_ris_api_dto.get("modified"),
            web=agenda_item_ris_api_dto.get("web"),
            deleted=agenda_item_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "meeting": self.meeting,
            "number": self.number,
            "order": self.order,
            "name": self.name,
            "public": self.public,
            "consultation": self.consultation,
            "result": self.result,
            "resolution_text": self.resolution_text,
            "resolution_file": (
                self.resolution_file.to_dict() if self.resolution_file else None
            ),
            "auxiliary_file": (
                [file.to_dict() for file in self.auxiliary_file]
                if self.auxiliary_file
                else None
            ),
            "start": self.start,
            "end": self.end,
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
            # "meeting": self.meeting,
            "number": self.number,
            "order": self.order,
            "name": self.name,
            "public": self.public,
            # "consultation": self.consultation,
            "result": self.result,
            "resolution_text": self.resolution_text,
            # "resolution_file": self.resolution_file,
            # "auxiliary_file": self.auxiliary_file,
            "start": self.start,
            "end": self.end,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
