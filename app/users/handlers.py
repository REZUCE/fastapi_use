from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body, Depends

from app.core.exception import UserAlreadyExistsException
from app.dependency import get_user_service
from app.users.schemas import UserSignInSchema, UserCreateSchema
from app.users.service import UserService

user_router = APIRouter(
    tags=["User"]
)

users = {}


@user_router.post("/signup")
async def sign_new_user(
        user_service: Annotated[UserService, Depends(get_user_service)],
        body: UserCreateSchema = Body(...)
) -> dict:
    try:
        await user_service.create_user(body)
        return {
            "message": "User successfully registered!"
        }
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e))


@user_router.post("/signin")
async def sign_user_in(user: UserSignInSchema) -> dict:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Wrong credentials passed"
        )
    return {
        "message": "User signed in successfully"
    }
