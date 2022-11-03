import logging

import hashlib
import jwt
from typing import Dict, Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from decouple import config, UndefinedValueError
from app.config import microservice
from pydantic import BaseModel

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    JWT_SECRET = config("SECRET")
    JWT_SECRET_SALT = f"{JWT_SECRET}-lsd93ufifmdk934mI79wsu"
    JWT_ALGORITHM = 'HS256'
except UndefinedValueError as e:
    logger.error(f"SECRET environment variable not defined. {str(e)}")
    exit(1)


class ApiKeyPayload(BaseModel):
    payload: str

    def __eq__(self, other):
        return self.payload == api_key_hash(other)


def api_key_hash(value) -> str:
    return hashlib.md5(f"{value}{JWT_SECRET_SALT}".encode()).hexdigest()


def sign_jwt(payload: str) -> Dict[str, str]:
    token = jwt.encode({"payload": payload}, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return {
        "access_token": token
    }


def decode_jwt(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            decoded_value = decode_jwt(credentials.credentials)
            if not decoded_value:
                raise HTTPException(status_code=403, detail="Invalid token.")
            api_key = ApiKeyPayload(**decoded_value)
            if api_key != microservice.api_key:
                raise HTTPException(status_code=403, detail="Invalid token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
