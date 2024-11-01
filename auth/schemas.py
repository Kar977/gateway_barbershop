from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    sub: str = None
    permissions: Optional[list[str]] = []
    roles: Optional[list[str]] = []
