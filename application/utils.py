from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, HTTPAuthorizationCredentials, HTTPBearer # 👈 new imports

from application.config import get_settings

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication"
        )
print("jol")
class VerifyToken:

    def __init__(self):
            self.config = get_settings()
            print("config", self.config)

            print("inside of verifytoken 1")
            jwks_url = f'https://{self.config.auth0_domain}/.well-known/jwks.json'
            self.jwks_client = jwt.PyJWKClient(jwks_url)

            print("inside of verifytoken 2")
    async def verify(self,
                     security_scopes: SecurityScopes,
                     token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer())
                     ):

        print("inside of verify func 1")
        if token is None:
            print("token is none")
            raise UnauthenticatedException

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt( #klucz publiczny
                token.credentials
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            print("raise unauthorized exception 1")
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            print("raise unauthorized exception 2")
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=self.config.auth0_algorithms,
                audience=self.config.auth0_api_audience,
                #issuer=self.config.auth0_issuer,
            )
        except Exception as error:
            "raise unauthorized exception 3"
            raise UnauthorizedException(str(error))

        return payload