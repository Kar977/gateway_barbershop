from auth.auth0_client import get_current_user as verify_if_logged
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.customer_manager.schemas import DeleteSlotRequest, SetSlotStatus
from settings import Settings

router = APIRouter(prefix="/slots")


@router.get("/available")
async def get_slots():

    return await send_request_to_service(
        "get",
        endpoint="/customers/slots/available/",
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.get("/available/{slot_date}")
async def get_slots_on_specific_date(slot_date: str):

    return await send_request_to_service(
        "get",
        endpoint=f"/customers/slots/available/{slot_date}",
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.put("/set")
async def set_slot_available(
    slot_request: SetSlotStatus, _: None = Security(verify_if_logged)
):
    await send_request_to_service(
        "put",
        endpoint="/customers/slot/status/",
        body_params=slot_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.delete("/slot/")
async def delete_slot(
    slot_request: DeleteSlotRequest, _: None = Security(verify_if_logged)
):
    await send_request_to_service(
        "delete",
        endpoint="/customers/slot/",
        body_params=slot_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
