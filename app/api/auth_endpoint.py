from fastapi import APIRouter, HTTPException
from starlette import status

from app import config
from app.api.auth.auth_bearer import sign_jwt, api_key_hash

router = APIRouter()

users = []


@router.get("/api-key/{api_key}", tags=["user"])
async def user_login(api_key: str):
    if api_key == config.microservice.api_key:
        return sign_jwt(api_key_hash(api_key))
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong Api Key")
