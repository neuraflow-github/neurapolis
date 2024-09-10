from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .location import Location
from .ris_api_dto import RisApiDto


class Organization(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    body: Optional[str]
    name: Optional[str]
    membership: Optional[List[str]]
    meeting: Optional[str]
    consultation: Optional[str]
    short_name: Optional[str]
    post: Optional[List[str]]
    sub_organization_of: Optional[str]
    organization_type: Optional[str]
    classification: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]
    website: Optional[str]
    location: Optional[Location]
    external_body: Optional[str]
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
        body: Optional[str],
        name: Optional[str],
        membership: Optional[List[str]],
        meeting: Optional[str],
        consultation: Optional[str],
        short_name: Optional[str],
        post: Optional[List[str]],
        sub_organization_of: Optional[str],
        organization_type: Optional[str],
        classification: Optional[str],
        start_date: Optional[str],
        end_date: Optional[str],
        website: Optional[str],
        location: Optional[Location],
        external_body: Optional[str],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[str],
        modified: Optional[str],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.body = body
        self.name = name
        self.membership = membership
        self.meeting = meeting
        self.consultation = consultation
        self.short_name = short_name
        self.post = post
        self.sub_organization_of = sub_organization_of
        self.organization_type = organization_type
        self.classification = classification
        self.start_date = start_date
        self.end_date = end_date
        self.website = website
        self.location = location
        self.external_body = external_body
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(organization_ris_api_dto: Dict) -> "Organization":
        return Organization(
            id=organization_ris_api_dto.get("id"),
            type=organization_ris_api_dto.get("type"),
            body=organization_ris_api_dto.get("body"),
            name=organization_ris_api_dto.get("name"),
            membership=organization_ris_api_dto.get("membership", []),
            meeting=organization_ris_api_dto.get("meeting"),
            consultation=organization_ris_api_dto.get("consultation"),
            short_name=organization_ris_api_dto.get("shortName"),
            post=organization_ris_api_dto.get("post", []),
            sub_organization_of=organization_ris_api_dto.get("subOrganizationOf"),
            organization_type=organization_ris_api_dto.get("organizationType"),
            classification=organization_ris_api_dto.get("classification"),
            start_date=organization_ris_api_dto.get("startDate"),
            end_date=organization_ris_api_dto.get("endDate"),
            website=organization_ris_api_dto.get("website"),
            location=(
                Location.from_ris_api_dto(organization_ris_api_dto.get("location"))
                if organization_ris_api_dto.get("location")
                else None
            ),
            external_body=organization_ris_api_dto.get("externalBody"),
            license=organization_ris_api_dto.get("license"),
            keyword=organization_ris_api_dto.get("keyword", []),
            created=organization_ris_api_dto.get("created"),
            modified=organization_ris_api_dto.get("modified"),
            web=organization_ris_api_dto.get("web"),
            deleted=organization_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "membership": self.membership,
            "meeting": self.meeting,
            "consultation": self.consultation,
            "short_name": self.short_name,
            "post": self.post,
            "sub_organization_of": self.sub_organization_of,
            "organization_type": self.organization_type,
            "classification": self.classification,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "website": self.website,
            "location": self.location.to_dict() if self.location else None,
            "external_body": self.external_body,
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
            "body": self.body,
            "name": self.name,
            # "membership": self.membership,
            # "meeting": self.meeting,
            # "consultation": self.consultation,
            "short_name": self.short_name,
            "post": self.post,
            # "sub_organization_of": self.sub_organization_of,
            "organization_type": self.organization_type,
            "classification": self.classification,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "website": self.website,
            # "location": self.location,
            "external_body": self.external_body,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
