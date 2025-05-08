from datetime import datetime

from auth.auth0_client import verify_employee_role
from fastapi import APIRouter, HTTPException, Security
from routers.common.connection import send_request_to_service
from routers.employees_manager.schemas import (
    CreateScheduleRequest,
    UpdateScheduleRequest,
    DeleteScheduleRequest,
)
from settings import Settings

router = APIRouter(prefix="/employee")


async def validate_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}")


@router.post("/schedule")
async def create_schedule(
    employee_request: CreateScheduleRequest, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/employee/schedule",
        body_params=employee_request,
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.get("/schedules")
async def list_schedules(_: None = Security(verify_employee_role)):
    return await send_request_to_service(
        "get",
        endpoint="/employee/schedules",
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.get("/schedules/start-date/{start}/end-date/{end}")
async def get_schedules_by_date_range(
    start: str, end: str, _: None = Security(verify_employee_role)
):
    start_date = await validate_date(start)
    end_date = await validate_date(end)
    return await send_request_to_service(
        "get",
        endpoint=f"/employee/schedules/start_date/{start_date}/end_date/{end_date}",
    )


@router.get("/schedules/day/{day}")
async def get_schedules_by_day(day: str, _: None = Security(verify_employee_role)):
    return await send_request_to_service(
        "get",
        endpoint=f"/employee/schedules/day/{day}",
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.get("/schedules/employee/{employee_id}")
async def get_schedules_by_specific_employee(
    employee_id: str, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "get",
        endpoint=f"/employee/schedules/employee/{employee_id}",
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.get("/schedule/employee/{employee_id}/day/{day}")
async def get_schedule_by_specific_employee_and_specific_day(
    employee_id: str, day: str, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "get",
        endpoint=f"/employee/schedule/employee/{employee_id}/day/{day}",
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.patch("/schedule")
async def update_schedule(
    schedule_request: UpdateScheduleRequest, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "patch",
        endpoint="/employee/schedule",
        body_params=schedule_request,
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/schedule")
async def delete_schedule(
    schedule_request: DeleteScheduleRequest, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "delete",
        endpoint="/employee/schedule",
        body_params=schedule_request,
        service_url=Settings.EMPLOYEE_MANAGER_MICROSERVICE_URL,
    )
