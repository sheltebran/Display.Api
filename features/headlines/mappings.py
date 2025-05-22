from features.headlines.models import Headline
from features.headlines.schemas import HeadlineDto
from typing import List

def map_headline_to_dto(headlines: List[Headline]):
    """Map headlines to DTOs
    Function to map the headlines to the DTOs for sending back to the caller.

    Parameters
    ----------
    headlines : List[Headline]
        List of the headlines obtained from the database

    Returns
    -------
    List[HeadlineDto]
        List of the DTOs to be sent back to the caller
    """
    headline_dto_list: List[HeadlineDto] = []

    for headline in headlines:
        headline_dto = HeadlineDto(heading=headline.heading, story=headline.story,
                       link=headline.link, pub_date=headline.pub_date,
                       league_id=headline.league_id
                       )
        headline_dto_list.append(headline_dto)

    return headline_dto_list

