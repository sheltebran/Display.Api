# Business logic
from api.external_routing import fetch_external_data
from fastapi import HTTPException
from features.headlines.models import Headline
from features.headlines.repository import add_headline, get_all_headlines
from features.leagues.repository import get_leagues, get_league_by_id
from features.headlines.schemas import HeadlineCreate
from typing import List

async def create_sport_headlines(sport_id: int):
    """Request to get and create new headlines

    This function accesses a sports headlines feed, parses the data
    and stores the result in a database, removing the old content.

    Parameters
    ----------
    sport_id : int
        Id for the sport and for accessing the different leagues and urls
        for the sports feed.

    Returns
    -------
    Result: bool
        A true setting indicates the creation was successful.
    """    

    leagues = await get_leagues(sport_id)

    if not leagues:
        raise HTTPException(status_code=404, detail=f"No leagues found for sport {sport_id}.")

    for league in leagues:
        headlines_dict = await import_headlines(league["league_id"])

        if not headlines_dict:
            raise HTTPException(status_code=404, detail=f"No headlines found for league {league['league_id']}.")
        
        for headline_dict in headlines_dict:
            row = await add_headline(headline_dict)
            if row is None:
                raise HTTPException(status_code=500, detail="Failed to add headline to database.")

async def get_headlines_by_league(league_id: int, limit: int = 10) -> List[Headline]:
    """Get all headlines

    Function to extract all headlines in the database for a league and send back
    to caller.

    Returns
    -------
    Headlines: List[tuple, Headlines]
        Tuple starting with string and followed by the Headline class.
    """

    headlines = await get_all_headlines(league_id, limit)

    return headlines

async def import_headlines(league_id: int):
    """Import the sport headlines from a RSS feed

    Parameters
    ----------
    league_id: int
    Id for the league

    Returns
    -------
    headlines: List[tuple, Headlines]
    Tuple starting with string and followed by the Headline class.

    """

    league = await get_league_by_id(league_id)

    if not league:
        raise HTTPException(status_code=404, detail=f"League with id {league_id} not found.")

    # call url and get headline data
    headlines_dict = await fetch_external_data(league["url"])

    # return list of headlines to be written
    return headlines_dict

