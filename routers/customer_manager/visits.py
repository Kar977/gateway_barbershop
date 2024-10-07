import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from routers.customer_manager.schemas import CreateVisitRequest


router = APIRouter(prefix="/visits")
MICROSERVICE_URL = "http://localhost:8001"


@router.post("/visit/")
async def create_visit(new_visit: CreateVisitRequest):

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{MICROSERVICE_URL}/customers/visit/", json=new_visit.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
