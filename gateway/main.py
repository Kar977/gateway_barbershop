from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from gateway.gateway.routers.customer_manager import slots, customers, visits, workday
from gateway.gateway.routers.users_manager import organization, users
from gateway.gateway.routers.employees_manager import employees


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")


def register_routers():
    import gateway.gateway.auth.auth0_client as auth0_client

    app.include_router(slots.router)
    app.include_router(customers.router)
    app.include_router(visits.router)
    app.include_router(workday.router)
    app.include_router(auth0_client.router)
    app.include_router(organization.router)
    app.include_router(users.router)
    app.include_router(employees.router)


register_routers()
