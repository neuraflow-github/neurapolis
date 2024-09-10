from typing import Optional

from pydantic import BaseModel


class FileChunkState(BaseModel):
    id: str
    text: str

    @classmethod
    def from_db_dict(cls, db_dict: dict) -> "FileChunkState":
        print("FileChunkState.from_db_dict")
        print(db_dict)
        print(db_dict.get("id"))
        print(db_dict.get("text"))
        return FileChunkState(
            id=db_dict.get("id"),
            text=db_dict.get("text"),
        )
