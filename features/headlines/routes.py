# FastAPI APIRouter
from fastapi import APIRouter, HTTPException
from features.headlines.mappings import map_headline_to_dto
from features.headlines.schemas import HeadlineCreate, Headline
from features.headlines.services import create_headlines, get_all_headlines
from typing import List

router = APIRouter(prefix="/headlines", tags=["Headlines"])

# Route to add new headlines
@router.post("/")
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
    result = await create_headlines(sport_id)

    if result is False:
        raise HTTPException(status_code=405, detail="Headline write did not work.")
    
    return {"headlines": "successful"} 

# Route to list all headlines
@router.get("/")
async def list_headlines(sport_id: int):
    headlines = get_all_headlines
    headline_dtos = map_headline_to_dto(headlines)
    return {headline_dtos}