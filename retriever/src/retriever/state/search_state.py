import uuid

from pydantic import BaseModel, Field

from .hit_state import HitState
from .search_step import SearchStep
from .search_type import SearchType


class SearchState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step: SearchStep
    type: SearchType
    query: str
    hits: list[HitState] = Field(default=[])
