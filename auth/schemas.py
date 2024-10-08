from pydantic import BaseModel

class TokenData(BaseModel):
    sub: str = None
    permissions: list[str] = []