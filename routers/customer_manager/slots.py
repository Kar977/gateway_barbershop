import httpx
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Request
from routers.customer_manager.schemas import SetSlotAvailable, DeleteSlotRequest

from settings import Settings

router = APIRouter(prefix="/slots")
ALLOWED_METHODS = ["get", "post", "put", "delete"]


async def send_request_to_service(
    method_name: str, endpoint: str, body_params=None, service_url=str
):  # ToDo gdzie wrzucic ta funkcje?

    if method_name not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported HTTP method: {method_name}")

    async with httpx.AsyncClient() as client:
        client_method = getattr(client, method_name)

        request_args = {"json": body_params.dict()} if body_params else {}

        try:
            response = await client_method(f"{service_url}{endpoint}", **request_args)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.response.text
            )


@router.get("/all/available")
async def get_slots():

    return await send_request_to_service(
        "get",
        endpoint="/customers/slots/all/available/",
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.get("/on/{slot_date}/available/")
async def get_slots_on_specific_date(slot_date: str):

    return await send_request_to_service(
        "get",
        endpoint=f"/customers/slots/{slot_date}/available/",
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.put("/set/available/")
async def set_slot_available(slot_request: SetSlotAvailable, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    await send_request_to_service(
        "put",
        endpoint="/customers/slot/set/available/",
        body_params=slot_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.delete("/slot/")
async def delete_slot(slot_request: DeleteSlotRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    await send_request_to_service(
        "delete",
        endpoint="/customers/slot/",
        body_params=slot_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
