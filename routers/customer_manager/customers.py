import httpx
from fastapi import APIRouter, Request
from fastapi import HTTPException
from routers.customer_manager.schemas import DeleteCustomerRequest


router = APIRouter(prefix="/customers")
MICROSERVICE_URL = "http://localhost:8001"


@router.delete("/customer/")
async def delete_customer(customer_request: DeleteCustomerRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged
    check_if_logged(request)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request("DELETE",f"{MICROSERVICE_URL}/customers/customer/", json=customer_request.dict())
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=exc.response.text)
