#from urllib.request import Request
from settings import Settings
from fastapi import APIRouter, Security, Request
import requests
import jwt
from starlette.exceptions import HTTPException
from main import oauth
from fastapi.responses import RedirectResponse
from starlette.responses import Response


router = APIRouter(prefix="/auth0")


print("oAuth0 ++++++++++++++++++=", oauth, flush=True)

# TODO move to another file
def verify_token(token: str):
    jwks_url = f"https://{Settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    jwks = requests.get(jwks_url).json()["keys"]
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=Settings.AUTH0_AUDIENCE,
            issuer=f"https://{Settings.AUTH0_DOMAIN}/",
        )
        return payload
    else:
        raise HTTPException(status_code=401, detail="Token is invalid")




@router.get("/api/public/")
def public():
    """No access token required to access this route"""

    result = {
        "status": "success",
        "msg": ("Hello from a public endpoint! You don't need to be "
                "authenticated to see this.")
    }
    return result


# Zabezpieczony endpoint - tylko zalogowani użytkownicy
@router.get("/private")
async def private_route(token: dict = Security(verify_token)):
    # Token dostępu będzie weryfikowany i zwrócone będą informacje o użytkowniku
    return {"message": "You are viewing a protected route!"}


# Punkt wejścia do logowania – przekierowanie do Auth0
@router.get("/login", response_model=None)
async def login(request: Request) -> RedirectResponse:
    redirect_uri = Settings.AUTH0_CALLBACK_URL
    return await oauth.auth0.authorize_redirect(request, redirect_uri)

# Callback po zalogowaniu użytkownika
@router.get("/callback")
async def callback(request: Request):
    # Weryfikacja kodu zwróconego przez Auth0 i uzyskanie tokenu dostępu
    print("callback - przed await", flush=True)
    token = await oauth.auth0.authorize_access_token(request)
    user_info = token["userinfo"]

    return {"token": token, "user_info": user_info}

