from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class LegislativeTerm(RisApiDto, DbDict):
    id: Optional[str]
    url: Optional[str]
    type: Optional[str]
    body: Optional[str]
    name: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    license: Optional[str]
    keyword: Optional[List[str]]
    created: Optional[datetime]
    modified: Optional[datetime]
    web: Optional[str]
    deleted: Optional[bool]

    def __init__(
        self,
        id: Optional[str],
        url: Optional[str],
        type: Optional[str],
        body: Optional[str],
        name: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.url = url
        self.type = type
        self.body = body
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(legislative_term_ris_api_dto: Dict) -> "LegislativeTerm":
        return LegislativeTerm(
            id=legislative_term_ris_api_dto.get("id"),
            url=legislative_term_ris_api_dto.get("url"),
            type=legislative_term_ris_api_dto.get("type"),
            body=legislative_term_ris_api_dto.get("body"),
            name=legislative_term_ris_api_dto.get("name"),
            start_date=legislative_term_ris_api_dto.get("startDate"),
            end_date=legislative_term_ris_api_dto.get("endDate"),
            license=legislative_term_ris_api_dto.get("license"),
            keyword=legislative_term_ris_api_dto.get("keyword"),
            created=legislative_term_ris_api_dto.get("created"),
            modified=legislative_term_ris_api_dto.get("modified"),
            web=legislative_term_ris_api_dto.get("web"),
            deleted=legislative_term_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "url": self.url,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
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
            "url": self.url,
            "type": self.type,
            # "body": self.body,
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
