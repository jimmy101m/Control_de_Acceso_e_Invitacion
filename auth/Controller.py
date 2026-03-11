from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from database.database import DBDependency
from auth.Models import Token
from auth.Service import authenticate_user, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: DBDependency
):
    user = await authenticate_user(form_data.username, form_data.password, db)
    roles = [role.name for role in user.roles]
    token = create_access_token(user.email, user.id, roles, timedelta(minutes=20))
    return Token(
        access_token=token,
        token_type='bearer'
    )
