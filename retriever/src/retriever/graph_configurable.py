from pydantic import BaseModel


class GraphConfigurable(BaseModel):
    search_count: int
    search_top_k: int
