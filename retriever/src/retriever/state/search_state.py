from pydantic import BaseModel

from .file_state import FileState
from .search_type import SearchType


class SearchState(BaseModel):
    id: str
    type: SearchType
    query: str
    files: list[FileState] = []
