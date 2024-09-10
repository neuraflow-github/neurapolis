import uuid
from typing import Optional

from pydantic import BaseModel, Field

from .file_chunk_state import FileChunkState
from .file_section_state import FileSectionState
from .grading_state import GradingState
from .hit_step import HitStep
from .related_data_state import RelatedDataState


class HitState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    step: HitStep
    file_chunk: FileChunkState
    file_section: Optional[FileSectionState] = Field(default=None)
    is_doubled: Optional[bool] = Field(default=None)
    text: Optional[str] = Field(default=None)
    node_data: Optional[dict] = Field(default=None)
    grading: Optional[GradingState] = Field(default=None)
    related_data: Optional[list[RelatedDataState]] = Field(default=None)

    def format_to_text(self) -> str:
        return self.file_section.text

    @staticmethod
    def format_hits_to_inner_xml(hits: list["HitState"]) -> str:
        formatted_hits = []
        for x_hit_index, x_hit in enumerate(hits):
            formatted_hits.append(
                f"<Treffer {x_hit_index + 1}>\n{x_hit.format_to_text()}\n</Treffer {x_hit_index + 1}>"
            )
        return "\n".join(formatted_hits)
