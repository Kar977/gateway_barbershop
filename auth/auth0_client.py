import httpx
from auth.schemas import TokenData
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from main import oauth
from settings import Settings

ALGORITHMS = ["RS256"]

router = APIRouter(prefix="/auth0")


async def get_auth0_public_key() -> list[dict]:
    jwks_url = f"https://{Settings.AUTH0_DOMAIN}/.well-known/jwks.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_url)
        jwks = response.json()

    return jwks["keys"]


async def verify_access_token(token: str) -> TokenData:
    try:
        jwks = await get_auth0_public_key()
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
                algorithms=ALGORITHMS,
                audience=Settings.AUTH0_API_AUDIENCE,
                issuer=f"https://{Settings.AUTH0_DOMAIN}/",
            )

            roles = payload.get(f"{Settings.AUTH0_DOMAIN}/roles", [])
            permissions = payload.get("permissions", [])

            return TokenData(sub=payload["sub"], roles=roles, permissions=permissions)
        else:
            raise HTTPException(status_code=401, detail="Invalid key.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    except KeyError as e:
        raise HTTPException(
            status_code=400, detail=f"Malformed token or missing key: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unexpected error: {str(e)}"
        )  # ToDo change detailed information on general info before release on production


async def get_current_user(request: Request) -> TokenData:
    token = request.session.get("access_token")

    if not token:
        raise HTTPException(status_code=403, detail="Missing token")
    return await verify_access_token(token)


async def check_role(request: Request, roles: list) -> list[str]:
    token = request.session.get("access_token")

    if not token:
        raise HTTPException(status_code=403, detail="Missing token")

    user_roles = await verify_access_token(token).roles

    if not any(role in user_roles for role in roles):
        raise HTTPException(
            status_code=401,
            detail=f"Access denied. Roles required = {roles}. Your roles = {user_roles}",
        )

    return user_roles


@router.get("/login", response_model=None)
async def login(request: Request) -> RedirectResponse:
    redirect_uri = Settings.AUTH0_CALLBACK_URL
    return await oauth.auth0.authorize_redirect(
        request, redirect_uri, audience=Settings.AUTH0_API_AUDIENCE
    )


@router.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user_info = token.get("userinfo")

    request.session["access_token"] = token["access_token"]

    return {"token": token, "user_info": user_info}


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return {"detail": "Logged out successfully"}


@router.get("/private")
async def private(request: Request):
    await get_current_user(request)

    return {"view": "private"}


@router.get("/private/roles")
async def private_roles(request: Request):
    await check_role(request, ["business-owner"])

    return {"message": "You are able to see it, because you have business-owner role!"}
