import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi.params import Security
from application.utils import VerifyToken

from routers.customer_manager.schemas import SetSlotAvailable, DeleteSlotRequest

router = APIRouter(prefix="/slots")
MICROSERVICE_URL = "http://localhost:8001"

auth = VerifyToken()


@router.get("/slots/all/available")
async def get_slots(auth_result: str = Security(auth.verify)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MICROSERVICE_URL}/customers/slots/all/available/")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)




@router.get("/slots/on/{slot_date}/available/")
async def get_slots_on_specific_date(slot_date: str, auth_result: str = Security(auth.verify)):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MICROSERVICE_URL}/customers/slots/{slot_date}/available/")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)



@router.put("/slots/set/available/")
async def set_slot_available(slot_request: SetSlotAvailable):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{MICROSERVICE_URL}/customers/slot/set/available/", json=slot_request.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.delete("/slots/slot/")
async def delete_slot(slot_request: DeleteSlotRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request("DELETE", f"{MICROSERVICE_URL}/customers/slot/", json=slot_request.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
