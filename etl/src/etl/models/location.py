from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class Location(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    description: Optional[str]
    geojson: Optional[Dict]
    street_address: Optional[str]
    room: Optional[str]
    postal_code: Optional[str]
    sub_locality: Optional[str]
    locality: Optional[str]
    bodies: Optional[List[str]]
    organizations: Optional[List[str]]
    persons: Optional[List[str]]
    meetings: Optional[List[str]]
    papers: Optional[List[str]]
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
        description: Optional[str],
        geojson: Optional[Dict],
        street_address: Optional[str],
        room: Optional[str],
        postal_code: Optional[str],
        sub_locality: Optional[str],
        locality: Optional[str],
        bodies: Optional[List[str]],
        organizations: Optional[List[str]],
        persons: Optional[List[str]],
        meetings: Optional[List[str]],
        papers: Optional[List[str]],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.description = description
        self.geojson = geojson
        self.street_address = street_address
        self.room = room
        self.postal_code = postal_code
        self.sub_locality = sub_locality
        self.locality = locality
        self.bodies = bodies
        self.organizations = organizations
        self.persons = persons
        self.meetings = meetings
        self.papers = papers
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(location_ris_api_dto: Dict) -> "Location":
        return Location(
            id=location_ris_api_dto.get("id"),
            type=location_ris_api_dto.get("type"),
            description=location_ris_api_dto.get("description"),
            geojson=location_ris_api_dto.get("geojson"),
            street_address=location_ris_api_dto.get("streetAddress"),
            room=location_ris_api_dto.get("room"),
            postal_code=location_ris_api_dto.get("postalCode"),
            sub_locality=location_ris_api_dto.get("subLocality"),
            locality=location_ris_api_dto.get("locality"),
            bodies=location_ris_api_dto.get("bodies"),
            organizations=location_ris_api_dto.get("organizations"),
            persons=location_ris_api_dto.get("persons"),
            meetings=location_ris_api_dto.get("meetings"),
            papers=location_ris_api_dto.get("papers"),
            license=location_ris_api_dto.get("license"),
            keyword=location_ris_api_dto.get("keyword"),
            created=location_ris_api_dto.get("created"),
            modified=location_ris_api_dto.get("modified"),
            web=location_ris_api_dto.get("web"),
            deleted=location_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "description": self.description,
            "geojson": self.geojson,
            "street_address": self.street_address,
            "room": self.room,
            "postal_code": self.postal_code,
            "sub_locality": self.sub_locality,
            "locality": self.locality,
            "bodies": self.bodies,
            "organizations": self.organizations,
            "persons": self.persons,
            "meetings": self.meetings,
            "papers": self.papers,
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
            "description": self.description,
            # "geojson": self.geojson,
            "street_address": self.street_address,
            "room": self.room,
            "postal_code": self.postal_code,
            "sub_locality": self.sub_locality,
            "locality": self.locality,
            # "bodies": self.bodies,
            # "organizations": self.organizations,
            # "persons": self.persons,
            # "meetings": self.meetings,
            # "papers": self.papers,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
