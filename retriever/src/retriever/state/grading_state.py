from pydantic import BaseModel


class GradingState(BaseModel):
    is_relevant: bool
    feedback: str
