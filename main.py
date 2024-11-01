from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware

from routers.customer_manager import slots, customers, visits, workday
from routers.users_manager import organization, users
from settings import Settings

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")
config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name="auth0",
    client_id=Settings.AUTH0_CLIENT_ID,
    client_secret=Settings.AUTH0_CLIENT_SECRET,
    authorize_url=f"https://{Settings.AUTH0_DOMAIN}/authorize",
    access_token_url=f"https://{Settings.AUTH0_DOMAIN}/oauth/token",
    redirect_uri=Settings.AUTH0_CALLBACK_URL,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{Settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


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
