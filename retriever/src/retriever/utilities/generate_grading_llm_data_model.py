import re
import uuid
from typing import Optional

from pydantic import BaseModel, Field, create_model


def generate_grading_llm_data_model(count: int) -> type:
    fields = {}
    for i in range(1, count + 1):
        relevance_field_name = f"is_hit_{i}_relevant"
        feedback_field_name = f"hit_{i}_feedback"
        fields[relevance_field_name] = (
            bool,
            Field(default=False, description=f"Is the {i}. hit relevant?"),
        )
        fields[feedback_field_name] = (
            Optional[str],
            Field(
                default="",
                description=f"Very short feedback on why the {i}. hit is relevant or not.",
            ),
        )
    model_name = "GradingLlmDataModel" + re.sub("[^a-zA-Z]", "", str(uuid.uuid4()))
    return create_model(model_name, **fields)
