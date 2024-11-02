from auth.auth0_client import get_current_user as verify_if_logged
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.customer_manager.schemas import CreateVisitRequest
from settings import Settings

router = APIRouter(prefix="/visits")


@router.post("/visit/")
async def create_visit(
    new_visit: CreateVisitRequest, _: None = Security(verify_if_logged)
):
    await send_request_to_service(
        "post",
        endpoint="/customers/visit/",
        body_params=new_visit,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
