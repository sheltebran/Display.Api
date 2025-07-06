from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

@app.get("/fetch-external-data/")
async def fetch_external_data(external_url: str):
    """
    Calls an external URL and returns its content.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            return response.json()  # Assuming the external API returns JSON
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting {exc.request.url!r}.")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
