from typing import List,Optional
from langchain_core.pydantic_v1 import BaseModel, Field

class Assign(BaseModel):
    """Information about a Assign Event."""

    crewProfileId: Optional[int] = Field(..., description="Crew Id.")
    eventId: Optional[int] = Field(..., description="Event Id.")
    days: Optional[List[str]] = Field(..., description="The List on Days")