from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .membership import Membership
from .ris_api_dto import RisApiDto


class Person(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    body: Optional[str]
    name: Optional[str]
    family_name: Optional[str]
    given_name: Optional[str]
    form_of_address: Optional[str]
    affix: Optional[str]
    title: Optional[List[Optional[str]]]
    gender: Optional[str]
    phone: Optional[List[Optional[str]]]
    email: Optional[List[Optional[str]]]
    location: Optional[str]
    location_object: Optional[str]
    status: Optional[List[Optional[str]]]
    membership: Optional[List[Membership]]
    life: Optional[str]
    life_source: Optional[str]
    license: Optional[str]
    keyword: Optional[List[Optional[str]]]
    created: Optional[datetime]
    modified: Optional[datetime]
    web: Optional[str]
    deleted: Optional[bool]

    def __init__(
        self,
        id: Optional[str] = None,
        type: Optional[str] = None,
        body: Optional[str] = None,
        name: Optional[str] = None,
        family_name: Optional[str] = None,
        given_name: Optional[str] = None,
        form_of_address: Optional[str] = None,
        affix: Optional[str] = None,
        title: Optional[List[Optional[str]]] = None,
        gender: Optional[str] = None,
        phone: Optional[List[Optional[str]]] = None,
        email: Optional[List[Optional[str]]] = None,
        location: Optional[str] = None,
        location_object: Optional[str] = None,
        status: Optional[List[Optional[str]]] = None,
        membership: Optional[List[Membership]] = None,
        life: Optional[str] = None,
        life_source: Optional[str] = None,
        license: Optional[str] = None,
        keyword: Optional[List[Optional[str]]] = None,
        created: Optional[str] = None,
        modified: Optional[str] = None,
        web: Optional[str] = None,
        deleted: Optional[bool] = None,
    ):
        self.id = id
        self.type = type
        self.body = body
        self.name = name
        self.family_name = family_name
        self.given_name = given_name
        self.form_of_address = form_of_address
        self.affix = affix
        self.title = title
        self.gender = gender
        self.phone = phone
        self.email = email
        self.location = location
        self.location_object = location_object
        self.status = status
        self.membership = membership
        self.life = life
        self.life_source = life_source
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(person_ris_api_dto: Dict) -> "Person":
        return Person(
            id=person_ris_api_dto.get("id"),
            type=person_ris_api_dto.get("type"),
            body=person_ris_api_dto.get("body"),
            name=person_ris_api_dto.get("name"),
            family_name=person_ris_api_dto.get("familyName"),
            given_name=person_ris_api_dto.get("givenName"),
            form_of_address=person_ris_api_dto.get("formOfAddress"),
            affix=person_ris_api_dto.get("affix"),
            title=person_ris_api_dto.get("title"),
            gender=person_ris_api_dto.get("gender"),
            phone=person_ris_api_dto.get("phone"),
            email=person_ris_api_dto.get("email"),
            location=person_ris_api_dto.get("location"),
            location_object=person_ris_api_dto.get("locationObject"),
            status=person_ris_api_dto.get("status"),
            membership=(
                [
                    Membership.from_ris_api_dto(x_membership_api_dto)
                    for x_membership_api_dto in person_ris_api_dto.get("membership")
                ]
                if person_ris_api_dto.get("membership")
                else None
            ),
            life=person_ris_api_dto.get("life"),
            life_source=person_ris_api_dto.get("lifeSource"),
            license=person_ris_api_dto.get("license"),
            keyword=person_ris_api_dto.get("keyword"),
            created=person_ris_api_dto.get("created"),
            modified=person_ris_api_dto.get("modified"),
            web=person_ris_api_dto.get("web"),
            deleted=person_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "body": self.body,
            "name": self.name,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "form_of_address": self.form_of_address,
            "affix": self.affix,
            "title": self.title,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            "location": self.location,
            "location_object": self.location_object,
            "status": self.status,
            "membership": (
                [membership.to_dict() for membership in self.membership]
                if self.membership
                else None
            ),
            "life": self.life,
            "life_source": self.life_source,
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
            # "body": self.body,
            "name": self.name,
            "family_name": self.family_name,
            "given_name": self.given_name,
            "form_of_address": self.form_of_address,
            "affix": self.affix,
            "title": self.title,
            "gender": self.gender,
            "phone": self.phone,
            "email": self.email,
            # "location": self.location,
            "location_object": self.location_object,
            "status": self.status,
            # "membership": self.membership,
            "life": self.life,
            "life_source": self.life_source,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
