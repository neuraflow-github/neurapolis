from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .legislative_term import LegislativeTerm
from .location import Location
from .ris_api_dto import RisApiDto


class Body(RisApiDto, DbDict):
    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        system: Optional[str],
        short_name: Optional[str],
        name: Optional[str],
        website: Optional[str],
        license: Optional[str],
        license_valid_since: Optional[datetime],
        oparl_since: Optional[datetime],
        ags: Optional[str],
        rgs: Optional[str],
        equivalent: Optional[List[str]],
        contact_email: Optional[str],
        contact_name: Optional[str],
        organization: Optional[str],
        person: Optional[str],
        meeting: Optional[str],
        paper: Optional[str],
        legislative_term: Optional[List[LegislativeTerm]],
        agenda_item: Optional[str],
        consultation: Optional[str],
        file: Optional[str],
        location_list: Optional[str],
        legislative_term_list: Optional[str],
        membership: Optional[str],
        classification: Optional[str],
        location: Optional[Location],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.system = system
        self.short_name = short_name
        self.name = name
        self.website = website
        self.license = license
        self.license_valid_since = license_valid_since
        self.oparl_since = oparl_since
        self.ags = ags
        self.rgs = rgs
        self.equivalent = equivalent
        self.contact_email = contact_email
        self.contact_name = contact_name
        self.organization = organization
        self.person = person
        self.meeting = meeting
        self.paper = paper
        self.legislative_term = legislative_term
        self.agenda_item = agenda_item
        self.consultation = consultation
        self.file = file
        self.location_list = location_list
        self.legislative_term_list = legislative_term_list
        self.membership = membership
        self.classification = classification
        self.location = location
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(body_ris_api_dto: Dict) -> "Body":
        return Body(
            id=body_ris_api_dto.get("id"),
            type=body_ris_api_dto.get("type"),
            system=body_ris_api_dto.get("system"),
            short_name=body_ris_api_dto.get("shortName"),
            name=body_ris_api_dto.get("name"),
            website=body_ris_api_dto.get("website"),
            license=body_ris_api_dto.get("license"),
            license_valid_since=body_ris_api_dto.get("licenseValidSince"),
            oparl_since=body_ris_api_dto.get("oparlSince"),
            ags=body_ris_api_dto.get("ags"),
            rgs=body_ris_api_dto.get("rgs"),
            equivalent=body_ris_api_dto.get("equivalent"),
            contact_email=body_ris_api_dto.get("contactEmail"),
            contact_name=body_ris_api_dto.get("contactName"),
            organization=body_ris_api_dto.get("organization"),
            person=body_ris_api_dto.get("person"),
            meeting=body_ris_api_dto.get("meeting"),
            paper=body_ris_api_dto.get("paper"),
            legislative_term=(
                [
                    LegislativeTerm.from_ris_api_dto(x_legislative_term_ris_api_dto)
                    for x_legislative_term_ris_api_dto in body_ris_api_dto.get(
                        "legislativeTerm"
                    )
                ]
                if body_ris_api_dto.get("legislativeTerm")
                else None
            ),
            agenda_item=body_ris_api_dto.get("agendaItem"),
            consultation=body_ris_api_dto.get("consultation"),
            file=body_ris_api_dto.get("file"),
            location_list=body_ris_api_dto.get("locationList"),
            legislative_term_list=body_ris_api_dto.get("legislativeTermList"),
            membership=body_ris_api_dto.get("membership"),
            classification=body_ris_api_dto.get("classification"),
            location=(
                Location.from_ris_api_dto(body_ris_api_dto.get("location"))
                if body_ris_api_dto.get("location")
                else None
            ),
            keyword=body_ris_api_dto.get("keyword"),
            created=body_ris_api_dto.get("created"),
            modified=body_ris_api_dto.get("modified"),
            web=body_ris_api_dto.get("web"),
            deleted=body_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "system": self.system,
            "short_name": self.short_name,
            "name": self.name,
            "website": self.website,
            "license": self.license,
            "license_valid_since": self.license_valid_since,
            "oparl_since": self.oparl_since,
            "ags": self.ags,
            "rgs": self.rgs,
            "equivalent": self.equivalent,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "organization": self.organization,
            "person": self.person,
            "meeting": self.meeting,
            "paper": self.paper,
            "legislative_term": (
                [term.to_dict() for term in self.legislative_term]
                if self.legislative_term
                else None
            ),
            "agenda_item": self.agenda_item,
            "consultation": self.consultation,
            "file": self.file,
            "location_list": self.location_list,
            "legislative_term_list": self.legislative_term_list,
            "membership": self.membership,
            "classification": self.classification,
            "location": (
                self.location
                if isinstance(self.location, str)
                else self.location.to_dict() if self.location else None
            ),
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
            # "system": self.system,
            "short_name": self.short_name,
            "name": self.name,
            "website": self.website,
            "license": self.license,
            "license_valid_since": self.license_valid_since,
            "oparl_since": self.oparl_since,
            "ags": self.ags,
            "rgs": self.rgs,
            "equivalent": self.equivalent,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            # "organization": self.organization,
            # "person": self.person,
            # "meeting": self.meeting,
            # "paper": self.paper,
            # "legislative_term": self.legislative_term,
            # "agenda_item": self.agenda_item,
            # "consultation": self.consultation,
            # "file": self.file,
            # "location_list": self.location_list,
            # "legislative_term_list": self.legislative_term_list,
            # "membership": self.membership,
            # "classification": self.classification,
            # "location": self.location,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
