import httpx
from fastapi import HTTPException


BASE_URL = "https://api.artic.edu/api/v1/artworks"


async def fetch_artwork(external_id: int) -> dict:
    url = f"{BASE_URL}/{external_id}"

    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url)

    if response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Artwork not found in Art Institute API"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch data from Art Institute API"
        )

    data = response.json()

    artwork_data = data.get("data")
    if not artwork_data:
        raise HTTPException(
            status_code=502,
            detail="Unexpected response from Art Institute API"
        )

    return {
        "external_id": artwork_data["id"],
        "title": artwork_data.get("title", "Untitled")
    }
