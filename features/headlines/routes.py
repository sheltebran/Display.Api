# FastAPI APIRouter
from fastapi import APIRouter, HTTPException
from features.headlines.mappings import map_headline_to_dtos
from features.headlines.services import create_headlines_for_sport, get_headlines_by_league

router = APIRouter(prefix="/headlines", tags=["Headlines"])

@router.post("/{sport_id:int}")
async def create_headlines(sport_id: int):
    """Create headlines for a sport

    Parameters
    ----------
    sport_id : int
        The sport requested will be used to determine all leagues in the sport and headlines
        will be retrieved and filed for by league

    Returns
    -------
    OK: Status code 200
        A successful message will be sent

    Raises
    ------
    HTTPException: Status code 405 (Conflict)
        The message will state that the write did not work correctly
    """
    
    await create_headlines_for_sport(sport_id)
    
    return {"headlines": "successful"} 


@router.get("/{league_id:int}")
async def list_headlines(league_id: int):
    """List all headlines for a league
    Function to list all headlines for a league. The league id is passed
    in the URL and the function will extract all headlines for that league

    Parameters
    ----------
    league_id : int
        Id for the league to be used to extract all headlines
        for that league. The league id is passed in the URL.

        Returns
    -------
    List[Headline]
        List of the headlines for that league. The list is a list of
        tuples starting with a string and followed by the Headline class.
    """

    headlines_dto = await get_headlines_by_league(league_id, 10)

    if not headlines_dto:
        raise HTTPException(status_code=404, detail="No headlines found for this league.")
    
    return {"headlines": headlines_dto}
