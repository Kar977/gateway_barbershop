import pytest

from fastapi.testclient import TestClient
from main import app
from httpx import AsyncClient, ASGITransport
client = TestClient(app)


@pytest.mark.asyncio
async def test_create_schedule(mock_employee_request, override_employee_role):
    mock_employee_request({"employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/employee/schedule",
            json={
                "employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"}
        )

    assert response.status_code == 200
    assert response.json() == {"employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"}


@pytest.mark.asyncio
async def test_create_schedule_without_access(mock_employee_request):
    mock_employee_request({"employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/employee/schedule",
            json={
                "employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"}
        )

    assert response.status_code == 403
    assert "Missing token" in response.text