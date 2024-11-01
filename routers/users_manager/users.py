from fastapi import APIRouter, Request
from routers.customer_manager.slots import send_request_to_service
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
async def create_user(user_request: CreateUser, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "post",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/user")
async def delete_user(user_request: DeleteUserAccount, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "delete",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.get("/users")
async def get_all_user(request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner", "employee"])

    return await send_request_to_service(
        "get", endpoint="/users", service_url=Settings.USER_MANAGER_MICROSERVICE_URL
    )


@router.post("/password_change")
async def send_password_ticket_change(
    user_request: SetUserPasswordEmail, request: Request
):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "post",
        endpoint="/user/password_change",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.put("/user")
async def modify_user(user_request: ModifyUser, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "put",
        endpoint="/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.post("/invite")
async def delete_user(user_request: NewMember, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "post",
        endpoint="/send_invitation",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )
