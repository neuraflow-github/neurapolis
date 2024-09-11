from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class System(RisApiDto, DbDict):
    id: Optional[str]
    type: Optional[str]
    oparl_version: Optional[str]
    other_oparl_versions: Optional[List[str]]
    license: Optional[str]
    body: Optional[str]
    name: Optional[str]
    contact_email: Optional[str]
    contact_name: Optional[str]
    website: Optional[str]
    vendor: Optional[str]
    product: Optional[str]
    created: Optional[datetime]
    modified: Optional[datetime]
    web: Optional[str]
    deleted: Optional[bool]

    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        oparl_version: Optional[str],
        other_oparl_versions: Optional[List[str]],
        license: Optional[str],
        body: Optional[str],
        name: Optional[str],
        contact_email: Optional[str],
        contact_name: Optional[str],
        website: Optional[str],
        vendor: Optional[str],
        product: Optional[str],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.oparl_version = oparl_version
        self.other_oparl_versions = other_oparl_versions
        self.license = license
        self.body = body
        self.name = name
        self.contact_email = contact_email
        self.contact_name = contact_name
        self.website = website
        self.vendor = vendor
        self.product = product
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(system_ris_api_dto: Dict) -> "System":
        return System(
            id=system_ris_api_dto.get("id"),
            type=system_ris_api_dto.get("type"),
            oparl_version=system_ris_api_dto.get("oparlVersion"),
            other_oparl_versions=system_ris_api_dto.get("otherOparlVersions"),
            license=system_ris_api_dto.get("license"),
            body=system_ris_api_dto.get("body"),
            name=system_ris_api_dto.get("name"),
            contact_email=system_ris_api_dto.get("contactEmail"),
            contact_name=system_ris_api_dto.get("contactName"),
            website=system_ris_api_dto.get("website"),
            vendor=system_ris_api_dto.get("vendor"),
            product=system_ris_api_dto.get("product"),
            created=system_ris_api_dto.get("created"),
            modified=system_ris_api_dto.get("modified"),
            web=system_ris_api_dto.get("web"),
            deleted=system_ris_api_dto.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "oparl_version": self.oparl_version,
            "other_oparl_versions": self.other_oparl_versions,
            "license": self.license,
            "body": self.body,
            "name": self.name,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "website": self.website,
            "vendor": self.vendor,
            "product": self.product,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }

    def to_db_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "oparl_version": self.oparl_version,
            "other_oparl_versions": self.other_oparl_versions,
            "license": self.license,
            # "body": self.body,
            "name": self.name,
            "contact_email": self.contact_email,
            "contact_name": self.contact_name,
            "website": self.website,
            "vendor": self.vendor,
            "product": self.product,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
