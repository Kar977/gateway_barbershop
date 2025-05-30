import pytest
from fastapi import Request

from auth.auth0_client import verify_employee_role, verify_business_owner_role
from main import app


@pytest.fixture
def override_employee_role():
    async def dummy_dependency(request: Request):
        return True
    app.dependency_overrides[verify_employee_role] = dummy_dependency
    yield
    app.dependency_overrides.pop(verify_employee_role, None)

@pytest.fixture
def override_business_owner_role():
    async def dummy_dependency(request: Request):
        return True
    app.dependency_overrides[verify_business_owner_role] = dummy_dependency
    yield
    app.dependency_overrides.pop(verify_business_owner_role, None)

import pytest
from unittest.mock import AsyncMock

@pytest.fixture
def mock_request(monkeypatch):
    def _mock_request(mocked_response: dict):
        async_mock = AsyncMock(return_value=mocked_response)

        monkeypatch.setattr(
            "routers.users_manager.organization.send_request_to_service",
            async_mock
        )
    return _mock_request

@pytest.fixture
def mock_employee_request(monkeypatch):
    def _mock_request(mocked_response: dict):
        async_mock = AsyncMock(return_value=mocked_response)

        monkeypatch.setattr(
            "routers.employees_manager.employees.send_request_to_service",
            async_mock
        )
    return _mock_request

@pytest.fixture
def mock_customer_request(monkeypatch):
    def _mock_request(mocked_response: dict):
        async_mock = AsyncMock(return_value=mocked_response)

        monkeypatch.setattr(
            "routers.customer_manager.workday.send_request_to_service",
            async_mock
        )
    return _mock_request