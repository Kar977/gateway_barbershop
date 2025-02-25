from auth.auth0_client import get_current_user as verify_if_logged
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.customer_manager.schemas import DeleteCustomerRequest
from settings import Settings

router = APIRouter(prefix="/customers")


@router.delete("/customer/")
async def delete_customer(
    customer_request: DeleteCustomerRequest, _: None = Security(verify_if_logged)
):
    await send_request_to_service(
        "delete",
        endpoint="/customers/customer/",
        body_params=customer_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
