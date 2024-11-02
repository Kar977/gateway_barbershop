from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from routers.customer_manager import slots, customers, visits, workday
from routers.users_manager import organization, users

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")


def register_routers():
    import auth.auth0_client as auth0_client

    app.include_router(slots.router)
    app.include_router(customers.router)
    app.include_router(visits.router)
    app.include_router(workday.router)
    app.include_router(auth0_client.router)
    app.include_router(organization.router)
    app.include_router(users.router)


register_routers()
