import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request

from routers.customer_manager.schemas import SetSlotAvailable, DeleteSlotRequest

router = APIRouter(prefix="/slots")
MICROSERVICE_URL = "http://localhost:8001"


@router.get("/all/available")
async def get_slots():

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MICROSERVICE_URL}/customers/slots/all/available/")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.get("/on/{slot_date}/available/")
async def get_slots_on_specific_date(slot_date: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{MICROSERVICE_URL}/customers/slots/{slot_date}/available/")
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.put("/set/available/")
async def set_slot_available(slot_request: SetSlotAvailable, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged
    check_if_logged(request)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{MICROSERVICE_URL}/customers/slot/set/available/", json=slot_request.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)


@router.delete("/slot/")
async def delete_slot(slot_request: DeleteSlotRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged
    check_if_logged(request)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request("DELETE", f"{MICROSERVICE_URL}/customers/slot/", json=slot_request.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
