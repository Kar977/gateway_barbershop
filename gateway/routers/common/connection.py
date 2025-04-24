import httpx
from fastapi import HTTPException

ALLOWED_METHODS = ["get", "post", "put", "delete"]


async def send_request_to_service(
    method_name: str, endpoint: str, body_params=None, service_url=str
):
    if method_name not in ALLOWED_METHODS:
        raise ValueError(f"Unsupported HTTP method: {method_name}")

    async with httpx.AsyncClient() as client:
        client_method = getattr(client, method_name)

        request_args = {"json": body_params.dict()} if body_params else {}

        try:
            response = await client_method(f"{service_url}{endpoint}", **request_args)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code, detail=exc.response.text
            )
