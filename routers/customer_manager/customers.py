from fastapi import APIRouter, Request
from routers.customer_manager.schemas import DeleteCustomerRequest
from routers.customer_manager.slots import send_request_to_service

from settings import Settings

router = APIRouter(prefix="/customers")


@router.delete("/customer/")
async def delete_customer(customer_request: DeleteCustomerRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    await send_request_to_service(
        "delete",
        endpoint="/customers/customer/",
        body_params=customer_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
