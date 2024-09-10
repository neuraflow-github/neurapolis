from pydantic import BaseModel


class FileChunkState(BaseModel):
    id: str
    file_section_id: str
    text: str

    @classmethod
    def from_db_dict(
        cls, file_chunk_db_dict: dict, file_section_id: str
    ) -> "FileChunkState":
        return cls(
            id=file_chunk_db_dict.get("id"),
            file_section_id=file_section_id,
            text=file_chunk_db_dict.get("text"),
        )
