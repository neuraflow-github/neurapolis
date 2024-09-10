from pydantic import BaseModel


class FileSectionState(BaseModel):
    id: str
    file_id: str
    text: str

    @classmethod
    def from_db_dict(cls, db_dict: dict) -> "FileSectionState":
        return cls(
            id=db_dict.get("id"),
            file_id=db_dict.get("file_id"),
            text=db_dict.get("text"),
        )
