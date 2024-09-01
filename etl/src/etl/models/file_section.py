from datetime import datetime
from typing import Dict, Optional

from .db_dict import DbDict


class FileSection(DbDict):
    def __init__(
        self,
        id: Optional[str],
        file_id: Optional[str],
        text: Optional[str],
        created_at: Optional[datetime],
        modified_at: Optional[datetime],
    ):
        self.id = id
        self.file_id = file_id
        self.text = text
        self.created_at = created_at
        self.modified_at = modified_at

    @staticmethod
    def from_db_dict(file_section_db_dict: Dict) -> "FileSection":
        return FileSection(
            id=file_section_db_dict.get("id"),
            file_id=file_section_db_dict.get("file_id"),
            text=file_section_db_dict.get("text"),
            created_at=file_section_db_dict.get("created_at"),
            modified_at=file_section_db_dict.get("modified_at"),
        )

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "file_id": self.file_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }

    def to_db_dict(self) -> Dict:
        return {
            "id": self.id,
            # "file_id": self.file_id,
            "text": self.text,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
        }
