from auth.auth0_client import verify_business_owner_role, verify_employee_role
from fastapi import APIRouter, Security
from routers.common.connection import send_request_to_service
from routers.users_manager.schemas import (
    CreateOrganization,
    OrganizationName,
    OrganizationIdentifier,
    ModifyOrganization,
    RemoveUserFromOrganization,
)
from settings import Settings

router = APIRouter(prefix="/organizations")


@router.post("/organization", status_code=201)
async def create_organization(
    user_request: CreateOrganization, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "post",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.get("/organization")
async def get_organization(
    user_request: OrganizationName, _: None = Security(verify_employee_role)
):
    return await send_request_to_service(
        "get",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/organization")
async def delete_organization(
    user_request: OrganizationIdentifier, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "delete",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.put("/organization")
async def update_organization(
    user_request: ModifyOrganization, _: None = Security(verify_business_owner_role)
):
    return await send_request_to_service(
        "put",
        endpoint="/organization",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )


@router.delete("/organization/user")
async def remove_user_from_organization(
    user_request: RemoveUserFromOrganization,
    _: None = Security(verify_business_owner_role),
):
    return await send_request_to_service(
        "delete",
        endpoint="/organization/user",
        body_params=user_request,
        service_url=Settings.USER_MANAGER_MICROSERVICE_URL,
    )
