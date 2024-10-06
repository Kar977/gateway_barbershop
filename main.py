from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from starlette.config import Config
from settings import Settings
from routers import customers_manager  # , employees_manager, entry_manager, rabbitmq, reporting_system, users_manager
from routers.customer_manager import slots, customers, visits, workday
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret-string")
config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name="auth0",
    client_id= Settings.AUTH0_CLIENT_ID,
    client_secret=Settings.AUTH0_CLIENT_SECRET,
    authorize_url=f"https://{Settings.AUTH0_DOMAIN}/authorize",
    access_token_url=f"https://{Settings.AUTH0_DOMAIN}/oauth/token",
    redirect_uri=Settings.AUTH0_CALLBACK_URL,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{Settings.AUTH0_DOMAIN}/.well-known/openid-configuration',
    )
    #jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
#)


def register_routers():
    import routers.auth0_test as auth0_test

    app.include_router(customers_manager.router)
    app.include_router(slots.router)
    app.include_router(customers.router)
    app.include_router(visits.router)
    app.include_router(workday.router)
    app.include_router(auth0_test.router)


register_routers()