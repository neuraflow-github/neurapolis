from typing import Annotated

from pydantic import BaseModel, Field

from .search_state import SearchState


def merge_searches(
    existing_searches: list[SearchState], new_searches: list[SearchState]
) -> list[SearchState]:
    merged_searches = {}
    for search in existing_searches:
        merged_searches[search.id] = search
    for new_search in new_searches:
        merged_searches[new_search.id] = new_search
    return list(merged_searches.values())


class State(BaseModel):
    query: str
    searches: Annotated[list[SearchState], merge_searches] = Field(default=[])
