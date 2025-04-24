import pytest

from fastapi.testclient import TestClient
from gateway.gateway.main import app
from httpx import AsyncClient, ASGITransport
client = TestClient(app)


@pytest.mark.asyncio
async def test_get_organization_by_name_without_access():
    response = client.request("GET","/organizations/organization", json={"name": "FirstOrganization"})

    assert response.status_code == 403
    assert "Missing token" in response.text

@pytest.mark.asyncio
async def test_create_organization(mock_request, override_business_owner_role):
    mock_request({"name": "FirstOrganization", "display_name":"GoodCut"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/organizations/organization",
            json={"name": "FirstOrganization", "display_name":"GoodCut"}
        )

    assert response.status_code == 201
    assert response.json() == {"name": "FirstOrganization", "display_name":"GoodCut"}


@pytest.mark.asyncio
async def test_create_organization_without_permission(mock_request):
    mock_request({"name": "FirstOrganization", "display_name": "GoodCut"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/organizations/organization",
            json={"name": "FirstOrganization", "display_name": "GoodCut"}
        )

    assert response.status_code == 403
    assert "Missing token" in response.text

@pytest.mark.asyncio
async def test_delete_organization(mock_request, override_business_owner_role):
    mock_request({"name": "FirstOrganization", "status": "deleted"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "DELETE",
            "/organizations/organization",
            json={"identifier": "FirstOrganization"}
        )

    assert response.status_code == 200
    assert "deleted" in response.text

@pytest.mark.asyncio
async def test_delete_organization_without_permission(mock_request):
    mock_request({"name": "FirstOrganization", "display_name": "GoodCut"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.request(
            "DELETE",
            "/organizations/organization",
            json={"identifier": "FirstOrganization"}
        )
    assert response.status_code == 403
    assert "Missing token" in response.text
