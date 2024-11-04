from auth.auth0_client import verify_business_owner_role, verify_employee_role
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.users_manager.schemas import (
    CreateUser,
    SetUserPasswordEmail,
    DeleteUserAccount,
    ModifyUser,
    NewMember,
)
from settings import Settings

router = APIRouter(prefix="/employees")


@router.post("/user")
async def create_user(
    user_request: CreateUser, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/user")
async def delete_user(
    user_request: DeleteUserAccount, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "delete",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.get("/users")
async def get_all_user(_: None = Security(verify_employee_role)):
    return await send_request_to_service(
        "get", endpoint="/users", service_url=Settings.USER_MANAGER_MICROSERVICE_URL
    )


@router.post("/password_change")
async def send_password_ticket_change(
    user_request: SetUserPasswordEmail, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/user/password_change",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.put("/user")
async def modify_user(
    user_request: ModifyUser, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "put",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.post("/invite")
async def delete_user(
    user_request: NewMember, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/send_invitation",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )
