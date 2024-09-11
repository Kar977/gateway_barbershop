from fastapi import FastAPI, APIRouter

import httpx
from fastapi import FastAPI, HTTPException


router = APIRouter()

# routers/
   # customers_manager/
     # slots.py
        # /slots/available ----> /slots/available in customers_manager

     # visits.py
        #

MICROSERVICE_URL = "http://localhost:8001"

@router.get("/customers")
async def get_home_from_microservice():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MICROSERVICE_URL}/customers")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)

@router.get("/main_view")
def get_main_view():
    pass
