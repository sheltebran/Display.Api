# SQLAlchemy or Pydantic models
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Headline:
    headline_id: int
    heading: str
    story: str
    link: str
    pub_date: datetime
    league_id: int
