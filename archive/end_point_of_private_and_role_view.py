"""

@router.get("/private")
async def private(request: Request):
    get_current_user(request)

    return {"view": "private"}


@router.get("/private/roles")
async def private_roles(request: Request):
    check_role(request, ["business-owner"])

    return {"message": "You are able to see it, because you have business-owner role!"}


"""


#Code with previous access_token taken from session (it means cookie), instead of Header position = X-Access-Token
"""
async def get_current_user(request: Request): #-> TokenData:
    token = request.session.get("access_token")



    if not token:
        raise HTTPException(status_code=403, detail="Missing token")
    return await verify_access_token(token)


async def check_role(request: Request, roles: list) -> list[str]:
    token = request.session.get("access_token")


    if not token:
        raise HTTPException(status_code=403, detail="Missing token")

    user_roles = await verify_access_token(token)

    if not any(role in user_roles.roles for role in roles):
        raise HTTPException(
            status_code=401,
            detail=f"Access denied. Roles required = {roles}. Your roles = {user_roles}",
        )

    return user_roles
    
    
@router.get("/callback")
async def callback(request: Request):
    token = await oauth.auth0.authorize_access_token(request)
    user_info = token.get("userinfo")

    request.session["access_token"] = token["access_token"]
 
    return {"token": token, "user_info": user_info}


"""