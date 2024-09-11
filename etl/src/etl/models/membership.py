from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class Membership(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    person: Optional[str]
    organization: Optional[str]
    role: Optional[str]
    voting_right: Optional[bool]
    start_date: Optional[str]
    end_date: Optional[str]
    on_behalf_of: Optional[str]
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
        person: Optional[str],
        organization: Optional[str],
        role: Optional[str],
        voting_right: Optional[bool],
        start_date: Optional[str],
        end_date: Optional[str],
        on_behalf_of: Optional[str],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[str],
        modified: Optional[str],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.person = person
        self.organization = organization
        self.role = role
        self.voting_right = voting_right
        self.start_date = start_date
        self.end_date = end_date
        self.on_behalf_of = on_behalf_of
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(membership_ris_api_dto: Dict) -> "Membership":
        return Membership(
            id=membership_ris_api_dto.get("id"),
            type=membership_ris_api_dto.get("type"),
            person=membership_ris_api_dto.get("person"),
            organization=membership_ris_api_dto.get("organization"),
            role=membership_ris_api_dto.get("role"),
            voting_right=membership_ris_api_dto.get("votingRight"),
            start_date=membership_ris_api_dto.get("startDate"),
            end_date=membership_ris_api_dto.get("endDate"),
            on_behalf_of=membership_ris_api_dto.get("onBehalfOf"),
            license=membership_ris_api_dto.get("license"),
            keyword=membership_ris_api_dto.get("keyword"),
            created=membership_ris_api_dto.get("created"),
            modified=membership_ris_api_dto.get("modified"),
            web=membership_ris_api_dto.get("web"),
            deleted=membership_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "person": self.person,
            "organization": self.organization,
            "role": self.role,
            "voting_right": self.voting_right,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "on_behalf_of": self.on_behalf_of,
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
            # "person": self.person,
            # "organization": self.organization,
            "role": self.role,
            "voting_right": self.voting_right,
            "start_date": self.start_date,
            "end_date": self.end_date,
            # "on_behalf_of": self.on_behalf_of,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
