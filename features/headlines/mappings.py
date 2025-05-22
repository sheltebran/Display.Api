from features.headlines.models import Headline
from features.headlines.schemas import HeadlineDto
from typing import List

def map_headline_to_dto(headlines: List[Headline]):

    headline_dto_list: List[HeadlineDto] = []

    for headline in headlines:
        headline_dto = HeadlineDto(heading=headline.heading, story=headline.story,
                       link=headline.link, pub_date=headline.pub_date,
                       league_id=headline.league_id
                       )
        headline_dto_list.append(headline_dto)

    return headline_dto_list

