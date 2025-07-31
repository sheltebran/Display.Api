# Business logic
from api.external_routing import fetch_external_data
from fastapi import HTTPException
from features.headlines.repository import add_headline, get_all_headlines, delete_headlines_for_league
from features.leagues.repository import get_leagues

async def create_headlines_for_sport(sport_id: int):
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
        headlines_list = await import_headlines(league["url"])

        if not headlines_list:
            raise HTTPException(status_code=404, detail=f"No headlines found for league {league['league_id']}.")
        
        # Clear existing headlines for the league
        await delete_headlines_for_league(league["league_id"])

        for headline_list in headlines_list:
            row = await add_headline(headline_list, league["league_id"])
            if row is None:
                raise HTTPException(status_code=500, detail="Failed to add headline to database.")


async def get_headlines_by_league(league_id: int, limit: int = 10):
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


async def import_headlines(url: str):
    """Import the sport headlines from a RSS feed

    Parameters
    ----------
    url: str
        The URL of the RSS feed to import headlines from

    Returns
    -------
    headlines: List[tuple, Headlines]
    Tuple starting with string and followed by the Headline class.

    """

    # call url and get headline data
    headlines_list = await fetch_external_data(url)

    # return list of headlines to be written
    return headlines_list

