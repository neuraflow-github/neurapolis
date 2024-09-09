from operator import add
from typing import Annotated

from pydantic import BaseModel

from .search_state import SearchState


class State(BaseModel):
    query: str
    searches: Annotated[list[SearchState], add] = []
