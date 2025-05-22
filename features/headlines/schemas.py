# Pydantic request/response DTOs
from dataclasses import dataclass
from typing import Annotated
from pydantic import BaseModel, AfterValidator
from datetime import datetime
from validators import is_greater_than_zero, is_not_null_or_empty, validate_datetime_string

class HeadlineCreate(BaseModel):
    heading: Annotated[str, AfterValidator(is_not_null_or_empty)]
    story: Annotated[str, AfterValidator(is_not_null_or_empty)]
    link: Annotated[str, AfterValidator(is_not_null_or_empty)]
    pub_date: Annotated[str, AfterValidator(validate_datetime_string)]
    league_id: Annotated[int, AfterValidator(is_greater_than_zero)]

class HeadlineResponse(HeadlineCreate):
    headline_id: int

@dataclass
class HeadlineDto:
    heading: str
    story: str
    link: str
    pub_date: datetime
    league_id: int
