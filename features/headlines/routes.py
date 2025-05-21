# FastAPI APIRouter

from fastapi import APIRouter, HTTPException
from features.headlines.schemas import HeadlineCreate, Headline
from typing import List
from features.headlines.services import create_headlines, get_all_headlines
from features.headlines.mappings import map_headline_to_dto

router = APIRouter(prefix="/headlines", tags=["Headlines"])

# Route to add new headlines
#@router.post("/", response_model=HeadlineResponse)
@router.post("/")
async def create_headlines(league_id: str):
    result = create_headlines(league_id)
    return {"headlines": "successful"} 

# Route to list all headlines
@router.get("/")
async def list_headlines():
    headlines = get_all_headlines
    headline_dtos = map_headline_to_dto(headlines)
    return {headline_dtos}