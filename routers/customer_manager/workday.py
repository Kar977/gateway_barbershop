from fastapi import APIRouter, Request
from routers.customer_manager.schemas import DeleteWorkdayRequest, CreateWorkdayRequest
from routers.customer_manager.slots import send_request_to_service

from settings import Settings

router = APIRouter(prefix="/workdays")
MICROSERVICE_URL = "http://localhost:8001"


@router.post("/workdays/workday/")
async def create_workday(workday_request: CreateWorkdayRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    return await send_request_to_service(
        "post",
        endpoint="/customers/workday/",
        body_params=workday_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.post("/workdays/workday/")
async def create_workday(workday_request: CreateWorkdayRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    return await send_request_to_service(
        "post",
        endpoint="/customers/workday/",
        body_params=workday_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.delete("/workdays/workday/")
async def delete_workday(workday_request: DeleteWorkdayRequest, request: Request):
    from auth.auth0_client import get_current_user as check_if_logged

    check_if_logged(request)

    return await send_request_to_service(
        "delete",
        endpoint="/customers/workday/",
        body_params=workday_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
