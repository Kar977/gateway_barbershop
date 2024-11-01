from fastapi import APIRouter, Request
from routers.customer_manager.schemas import CreateVisitRequest
from routers.customer_manager.slots import send_request_to_service

from settings import Settings

router = APIRouter(prefix="/visits")
MICROSERVICE_URL = "http://localhost:8001"


@router.post("/visit/")
async def create_visit(new_visit: CreateVisitRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    await send_request_to_service(
        "post",
        endpoint="/customers/visit/",
        body_params=new_visit,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
