import pytest

from fastapi.testclient import TestClient
from main import app
from httpx import AsyncClient, ASGITransport
client = TestClient(app)


@pytest.mark.asyncio
async def test_create_workday(mock_customer_request, override_employee_role):
    mock_customer_request({
        "date": "01.01.2025",
        "day_status": "open"
    })

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/workdays/workdays/workday/",
            json={
                "date": "01.01.2025",
                "day_status": "open"
            }
        )

    assert response.status_code == 200
    assert response.json() == {
                "date": "01.01.2025",
                "day_status": "open"
            }


@pytest.mark.asyncio
async def test_create_workday_without_access(mock_customer_request):
    mock_customer_request({"employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"})

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/workdays/workdays/workday/",
            json={
                "employee_id": "1",
                "full_name": "Adam Nowak",
                "day": "01.01.2025",
                "availability": "07:00-15:00"}
        )

    assert response.status_code == 403
    assert "Missing token" in response.text