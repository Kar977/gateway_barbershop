from authlib.integrations.starlette_client import OAuth
from gateway.gateway.settings import Settings
from starlette.config import Config

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
