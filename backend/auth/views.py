
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()
app = FastAPI()


@router.get('/basic-auth')
def demo_basic_auth_credentials(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "something",
        "username": credentials.username,
        "password": credentials.password,
    }

usernames_to_passwords = {
    "admin": "admin",
    "john": "password",
}

def get_auth_user_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password
    )

@router.get('/basic-auth')
def udername(
        auth_username: str = Depends(...)
):
    return {
        "message": f"Hi {auth_username}",
        "username": auth_username,
    }


app.include_router(router)
