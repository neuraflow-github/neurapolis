from pydantic import BaseModel


class FileChunkState(BaseModel):
    id: str
    file_section_id: str
    text: str

    @classmethod
    def from_db_dict(cls, db_dict: dict) -> "FileChunkState":
        return cls(
            id=db_dict.get("id"),
            file_section_id=db_dict.get("file_section_id"),
            text=db_dict.get("text"),
        )
