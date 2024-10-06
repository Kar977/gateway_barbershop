import os

import jwt
import requests
from auth.schemas import TokenData
from dotenv import load_dotenv
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from main import oauth
from settings import Settings
from starlette.exceptions import HTTPException

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
API_AUDIENCE = os.getenv("AUTH0_API_AUDIENCE")
ALGORITHMS = ["RS256"]

router = APIRouter(prefix="/auth0")


def get_auth0_public_key():
    """
    Function that retrieves the public RSA key from Auth0 for JWT signature verification.

    This key is necessary for verifying the JWT tokens issued by Auth0.
    The keys are fetched from the well-known JWKS endpoint provided by Auth0.

    :return: The public keys from the Auth0 JWKS endpoint.
    """
    jwks_url = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
    jwks = requests.get(jwks_url).json()
    return jwks['keys']


def verify_access_token(token: str):
    """
    Function that verifies an access token issued by Auth0.

    This function decodes and verifies the JWT token by:
    1. Fetching the public RSA keys from Auth0.
    2. Extracting the token's unverified header to get the key ID (kid).
    3. Matching the key ID (kid) with the appropriate RSA key from Auth0.
    4. Using the RSA key to verify the signature and decode the token's payload.
    5. Returning the token's subject (sub) and permissions (if present) in a structured TokenData object.

    :param token: The JWT token string to verify.
    :return: TokenData object containing 'sub' (subject) and optional 'permissions'.
    :raises: HTTPException if the token is invalid or expired.
    """
    try:
        jwks = get_auth0_public_key()
        unverified_header = jwt.get_unverified_header(token)
        print("unverified_header = ", unverified_header)
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
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            return TokenData(sub=payload["sub"], permissions=payload.get("permissions", []))
        else:
            raise HTTPException(status_code=401, detail="Invalid key.")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or out-of-date token.")


def get_current_user(request: Request):
    """
    Retrieves the current user by verifying the access_token from the session.

    :param request: The HTTP request containing the session.
    :return: Verified user data if the token is valid.
    :raises: HTTPException with status 403 if no token is found.
    """

    token = request.session.get('access_token')
    print(token)

    if not token:
        raise HTTPException(status_code=403, detail="Missing token")
    return verify_access_token(token)


@router.get("/login", response_model=None)
async def login(request: Request) -> RedirectResponse:
    """
    Initiates the Auth0 login flow by redirecting the user to the Auth0 authorization URL.

    :param request: The HTTP request object.
    :return: Redirects the user to Auth0 for authentication.
    """

    redirect_uri = Settings.AUTH0_CALLBACK_URL
    return await oauth.auth0.authorize_redirect(request,
                                                redirect_uri,
                                                audience=API_AUDIENCE)


@router.get("/callback")
async def callback(request: Request):
    """
    Handles the Auth0 callback after login, retrieves the access token, and stores it in the session.

    :param request: The HTTP request object.
    :return: A dictionary with the access token and user information.
    """

    token = await oauth.auth0.authorize_access_token(request)
    user_info = token["userinfo"]

    request.session['access_token'] = token['access_token']

    return {"token": token, "user_info": user_info}


@router.get("/logout")
async def logout(request: Request):
    """
    Logs the user out by clearing the session.

    :param request: The HTTP request object.
    :return: A message confirming the user has logged out.
    """

    request.session.clear()

    return {"message": "logged out successfully"}

# ToDO delete it after implementation of tests
# End point only for check if security with token works correctly
@router.get("/private")
async def private_route(current_user: TokenData = Depends(get_current_user)):
    return {"message": "You are logged in", "user": current_user.sub}