from auth.auth0_client import verify_employee_role
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.customer_manager.schemas import DeleteWorkdayRequest, CreateWorkdayRequest
from settings import Settings

router = APIRouter(prefix="/workdays")


@router.post("/workdays/workday/")
async def create_workday(
    workday_request: CreateWorkdayRequest, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/customers/workday/",
        body_params=workday_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )


@router.delete("/workdays/workday/")
async def delete_workday(
    workday_request: DeleteWorkdayRequest, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "delete",
        endpoint="/customers/workday/",
        body_params=workday_request,
        service_url=Settings.CUSTOMER_MANGER_MICROSERVICE_URL,
    )
