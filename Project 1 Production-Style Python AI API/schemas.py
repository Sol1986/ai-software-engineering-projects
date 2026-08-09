from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# define the schema for the business request
class BusinessRequest(BaseModel):
    business_request: str = Field(
        min_length = 10,
        max_length = 2000,
        description = "The business request to be processed by the AI model."

    )

    context: dict[str, str] = Field(
        default_factory = dict,
        description = "Additional context for the business request."
    )

# define the schema for the business response
class BusinessResponse(BaseModel):
    request_id: UUID
    answer: str
    model: str
    created_at: datetime

