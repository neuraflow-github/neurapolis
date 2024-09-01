from datetime import datetime
from typing import Dict, List, Optional

from .db_dict import DbDict
from .ris_api_dto import RisApiDto


class File(RisApiDto, DbDict):
    def __init__(
        self,
        id: Optional[str],
        type: Optional[str],
        name: Optional[str],
        file_name: Optional[str],
        mime_type: Optional[str],
        date: Optional[str],
        size: Optional[int],
        sha1_checksum: Optional[str],
        sha512_checksum: Optional[str],
        text: Optional[str],
        access_url: Optional[str],
        download_url: Optional[str],
        external_service_url: Optional[str],
        master_file: Optional[str],
        derivative_file: Optional[List[str]],
        file_license: Optional[str],
        meeting: Optional[List[str]],
        agenda_item: Optional[List[str]],
        paper: Optional[List[str]],
        license: Optional[str],
        keyword: Optional[List[str]],
        created: Optional[datetime],
        modified: Optional[datetime],
        web: Optional[str],
        deleted: Optional[bool],
    ):
        self.id = id
        self.type = type
        self.name = name
        self.file_name = file_name
        self.mime_type = mime_type
        self.date = date
        self.size = size
        self.sha1_checksum = sha1_checksum
        self.sha512_checksum = sha512_checksum
        self.text = text
        self.access_url = access_url
        self.download_url = download_url
        self.external_service_url = external_service_url
        self.master_file = master_file
        self.derivative_file = derivative_file
        self.file_license = file_license
        self.meeting = meeting
        self.agenda_item = agenda_item
        self.paper = paper
        self.license = license
        self.keyword = keyword
        self.created = created
        self.modified = modified
        self.web = web
        self.deleted = deleted

    @staticmethod
    def from_ris_api_dto(file_ris_api_dto: Dict) -> "File":
        return File(
            id=file_ris_api_dto.get("id"),
            type=file_ris_api_dto.get("type"),
            name=file_ris_api_dto.get("name"),
            file_name=file_ris_api_dto.get("fileName"),
            mime_type=file_ris_api_dto.get("mimeType"),
            date=file_ris_api_dto.get("date"),
            size=file_ris_api_dto.get("size"),
            sha1_checksum=file_ris_api_dto.get("sha1Checksum"),
            sha512_checksum=file_ris_api_dto.get("sha512Checksum"),
            text=file_ris_api_dto.get("text"),
            access_url=file_ris_api_dto.get("accessUrl"),
            download_url=file_ris_api_dto.get("downloadUrl"),
            external_service_url=file_ris_api_dto.get("externalServiceUrl"),
            master_file=file_ris_api_dto.get("masterFile"),
            derivative_file=file_ris_api_dto.get("derivativeFile"),
            file_license=file_ris_api_dto.get("fileLicense"),
            meeting=file_ris_api_dto.get("meeting"),
            agenda_item=file_ris_api_dto.get("agendaItem"),
            paper=file_ris_api_dto.get("paper"),
            license=file_ris_api_dto.get("license"),
            keyword=file_ris_api_dto.get("keyword"),
            created=file_ris_api_dto.get("created"),
            modified=file_ris_api_dto.get("modified"),
            web=file_ris_api_dto.get("web"),
            deleted=file_ris_api_dto.get("deleted"),
        )

    @staticmethod
    def from_db_dict(db_dict: Dict) -> "File":
        return File(
            id=db_dict.get("id"),
            type=db_dict.get("type"),
            name=db_dict.get("name"),
            file_name=db_dict.get("file_name"),
            mime_type=db_dict.get("mime_type"),
            date=db_dict.get("date"),
            size=db_dict.get("size"),
            sha1_checksum=db_dict.get("sha1_checksum"),
            sha512_checksum=db_dict.get("sha512_checksum"),
            text=db_dict.get("text"),
            access_url=db_dict.get("access_url"),
            download_url=db_dict.get("download_url"),
            external_service_url=db_dict.get("external_service_url"),
            master_file=None,  # Not stored in DB
            derivative_file=None,  # Not stored in DB
            file_license=db_dict.get("file_license"),
            meeting=None,  # Not stored in DB
            agenda_item=None,  # Not stored in DB
            paper=None,  # Not stored in DB
            license=db_dict.get("license"),
            keyword=db_dict.get("keyword"),
            created=db_dict.get("created"),
            modified=db_dict.get("modified"),
            web=db_dict.get("web"),
            deleted=db_dict.get("deleted"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "date": self.date,
            "size": self.size,
            "sha1_checksum": self.sha1_checksum,
            "sha512_checksum": self.sha512_checksum,
            "text": self.text,
            "access_url": self.access_url,
            "download_url": self.download_url,
            "external_service_url": self.external_service_url,
            "master_file": (
                self.master_file
                if isinstance(self.master_file, str)
                else self.master_file.to_dict() if self.master_file else None
            ),
            "derivative_file": (
                [
                    x_file if isinstance(x_file, str) else x_file.to_dict()
                    for x_file in self.derivative_file
                ]
                if self.derivative_file
                else None
            ),
            "file_license": self.file_license,
            "meeting": self.meeting,
            "agenda_item": self.agenda_item,
            "paper": self.paper,
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
            "file_name": self.file_name,
            "mime_type": self.mime_type,
            "date": self.date,
            "size": self.size,
            "sha1_checksum": self.sha1_checksum,
            "sha512_checksum": self.sha512_checksum,
            "text": self.text,
            "access_url": self.access_url,
            "download_url": self.download_url,
            "external_service_url": self.external_service_url,
            # "master_file": self.master_file,
            # "derivative_file": self.derivative_file,
            "file_license": self.file_license,
            # "meeting": self.meeting,
            # "agenda_item": self.agenda_item,
            # "paper": self.paper,
            "license": self.license,
            "keyword": self.keyword,
            "created": self.created,
            "modified": self.modified,
            "web": self.web,
            "deleted": self.deleted,
        }
