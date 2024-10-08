import jwt
import requests
from auth.schemas import TokenData
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from main import oauth
from settings import Settings
from starlette.exceptions import HTTPException

ALGORITHMS = ["RS256"]

router = APIRouter(prefix="/auth0")


def get_auth0_public_key():
    jwks_url = f'https://{Settings.AUTH0_DOMAIN}/.well-known/jwks.json'
    jwks = requests.get(jwks_url).json()
    return jwks['keys']


def verify_access_token(token: str):
    try:
        jwks = get_auth0_public_key()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=Settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{Settings.AUTH0_DOMAIN}/"
            )
            return TokenData(sub=payload["sub"], permissions=payload.get("permissions", []))
        else:
            raise HTTPException(status_code=401, detail="Invalid key.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Malformed token or missing key: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def get_current_user(request: Request):
    token = request.session.get('access_token')

    if not token:
        raise HTTPException(status_code=403, detail="Missing token")
    return verify_access_token(token)


@router.get("/login", response_model=None)
async def login(request: Request) -> RedirectResponse:
    redirect_uri = Settings.AUTH0_CALLBACK_URL
    return await oauth.auth0.authorize_redirect(request,
                                                redirect_uri,
                                                audience=Settings.AUTH0_API_AUDIENCE)


@router.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user_info = token["userinfo"]

    request.session['access_token'] = token['access_token']

    return {"token": token, "user_info": user_info}


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
