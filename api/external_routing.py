from fastapi import FastAPI, HTTPException
import httpx
import xmltodict

app = FastAPI()

@app.get("/fetch-external-data/")
async def fetch_external_data(external_url: str):
    """Calls an external URL and returns its content.

    Parameters
    ----------
    external_url : str
        The URL to fetch data from.

    Returns
    -------
    dict
        The content of the URL parsed as a dictionary.
    """
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(external_url)
            response.raise_for_status()
            xml_dict = xmltodict.parse(response.text)
            return xml_dict
        
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=f"An error occurred while requesting {exc.request.url!r}.")
    
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.")
