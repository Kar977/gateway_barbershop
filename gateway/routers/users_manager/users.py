from gateway.gateway.auth.auth0_client import verify_business_owner_role, verify_employee_role
from fastapi import APIRouter, Security
from gateway.gateway.routers.common.connection import send_request_to_service
from gateway.gateway.routers.users_manager.schemas import (
    CreateUser,
    SetUserPasswordEmail,
    DeleteUserAccount,
    ModifyUser,
    NewMember,
    AddRolesToUser,
)
from gateway.gateway.settings import Settings

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


@router.get("/user/id/{email}")
async def get_user_id_by_email(
    email: str, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "get",
        endpoint=f"/user/id/{email}",
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.get("/users")
async def get_all_user(_: None = Security(verify_employee_role)):
    return await send_request_to_service(
        "get", endpoint="/users", service_url=Settings.USER_MANAGER_MICROSERVICE_URL
    )


@router.post("/user/password-reset/request")
async def send_password_ticket_change(
    user_request: SetUserPasswordEmail, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/user/password-reset/request",
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


@router.post("/user/organization/invitation")
async def invite_user_to_organization(
    user_request: NewMember, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/user/organization/invitation",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.post("/user/roles")
async def add_roles_to_user(
    user_request: AddRolesToUser, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/user/roles",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )
