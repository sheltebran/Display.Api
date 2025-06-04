# Pydantic request/response DTOs
from dataclasses import dataclass
from datetime import datetime
from features.headlines.validators import is_greater_than_zero, is_not_null_or_empty, validate_datetime_string
from pydantic import AfterValidator
from typing import Annotated

@dataclass
class HeadlineCreate:
    heading: Annotated[str, AfterValidator(is_not_null_or_empty)]
    story: Annotated[str, AfterValidator(is_not_null_or_empty)]
    link: Annotated[str, AfterValidator(is_not_null_or_empty)]
    pub_date: Annotated[str, AfterValidator(validate_datetime_string)]
    league_id: Annotated[int, AfterValidator(is_greater_than_zero)]

@dataclass
class HeadlineResponse(HeadlineCreate):
    headline_id: int

@dataclass
class HeadlineDto:
    heading: str
    story: str
    link: str
    pub_date: datetime
    league_id: int
