from pydantic import BaseModel

from .grading_state import GradingState
from .related_data_state import RelatedDataState


class FileState(BaseModel):
    text: str
    node_data: dict
    grading: GradingState | None = None
    related_data: list[RelatedDataState] | None = None
