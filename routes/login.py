from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

login_router = APIRouter()  

class LoginRequest(BaseModel):
    username: str
    password: str
    merchant_name: str
    merchant_code: str

class LoginResult(BaseModel):
    access_token: str
    refresh_token: str
    username: str

class LoginResponse(BaseModel):
    code: int
    message: str
    result: Optional[LoginResult]

@login_router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    if request.username == "string" and request.password == "string":
        return LoginResponse(
            code=200,
            message="SUCCESS",
            result=LoginResult(
                access_token="mocked-access-token",
                refresh_token="mocked-refresh-token",
                username="abmis"
            )
        )
    raise HTTPException(status_code=401, detail="You are not authorized to view the resource")
