from pydantic import BaseModel

from .grading_state import GradingState


class RelatedDataState(BaseModel):
    text: str
    node_datas: list[dict]
    grading: GradingState | None = None
