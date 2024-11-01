from fastapi import APIRouter, Request
from routers.customer_manager.slots import send_request_to_service
from routers.users_manager.schemas import (
    CreateOrganization,
    OrganizationName,
    OrganizationIdentifier,
    ModifyOrganization,
)
from settings import Settings

router = APIRouter(prefix="/organizations")


@router.post("/organization")
async def create_organization(user_request: CreateOrganization, request: Request):
    from auth.auth0_client import check_role

    check_role(request, "business-owner")

    return await send_request_to_service(
        "post",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.get("/organization")
async def get_organization(user_request: OrganizationName, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner", "employee"])

    return await send_request_to_service(
        "get",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/organization")
async def delete_organization(user_request: OrganizationIdentifier, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "delete",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.put("/organization")
async def modify_organization(user_request: ModifyOrganization, request: Request):
    from auth.auth0_client import check_role

    check_role(request, ["business-owner"])

    return await send_request_to_service(
        "put",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )
