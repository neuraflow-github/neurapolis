import re
import uuid

from pydantic import BaseModel, Field


def generate_grading_llm_data_model(count: int) -> type:
    fields = {}
    for i in range(1, count + 1):
        relevance_field_name = f"is_article_{i}_relevant"
        feedback_field_name = f"article_{i}_feedback"
        fields[relevance_field_name] = Field(
            default=False, description=f"Is the {i}. article relevant?"
        )
        fields[feedback_field_name] = Field(
            default="",
            description=f"Very short feedback for the on why the {i}. article is relevant or not.",
        )
    return type(
        # "StoryRelevanceGraderLlmDataModel" + type_name_postfix, (BaseModel,), fields
        "GradingLlmDataModel" + re.sub("[^a-zA-Z]", "", str(uuid.uuid4())),
        (BaseModel,),
        fields,
    )
