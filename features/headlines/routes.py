# FastAPI APIRouter
from fastapi import APIRouter, HTTPException
from features.headlines.mappings import map_headline_to_dto
from features.headlines.services import create_sport_headlines, get_headlines_by_league
from typing import List

router = APIRouter(prefix="/headlines", tags=["Headlines"])

# Route to add new headlines
@router.post("/{sport_id:int}/")
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
    result = await create_sport_headlines(sport_id)

    if result is False:
        raise HTTPException(status_code=405, detail="Headline write did not work.")
    
    return {"headlines": "successful"} 

# Route to list all headlines
@router.get("/{league_id:int}/")
async def list_headlines(league_id: int):
    headlines = await get_headlines_by_league(league_id)
    headline_dtos = map_headline_to_dto(headlines)
    return {"headlines": headline_dtos}