from pydantic import BaseModel


class FileSectionState(BaseModel):
    id: str
    file_id: str
    text: str

    @classmethod
    def from_db_dict(
        cls, file_section_db_dict: dict, file_id: str
    ) -> "FileSectionState":
        return cls(
            id=file_section_db_dict.get("id"),
            file_id=file_id,
            text=file_section_db_dict.get("text"),
        )
