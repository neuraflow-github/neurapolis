import uuid

from pydantic import BaseModel, Field

from .file_chunk_state import FileChunkState
from .file_section_state import FileSectionState
from .grading_state import GradingState
from .related_data_state import RelatedDataState


class HitState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    file_chunk_id: str
    file_chunk: FileChunkState
    is_doubled: bool = Field(default=False)
    file_section_id: str
    file_section: FileSectionState = Field(default=None)
    text: str = Field(default=None)
    node_data: dict = Field(default=None)
    grading: GradingState | None = Field(default=None)
    related_data: list[RelatedDataState] | None = Field(default=None)

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
