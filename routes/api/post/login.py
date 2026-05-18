from typing import Annotated, Any, cast

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from jose import JWTError
from sqlalchemy import insert, select

from uuid import UUID, uuid4

from ...base_route import BaseRoute
from models.forms import UserResponse, UserLogin, Token
from models import User, UserProfile, UserCredentials, Role, RefreshToken
from db.db import db_dependency


class LoginRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'login'
        self.methods_type = "POST"

    async def endpoint(self, form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):

        response1 = (await db.execute(select(User).where(User.email==form_data.username))).scalar()

        if response1 is None:
            raise HTTPException(status_code=400, detail="Неверный email или пароль")
        
        response2 = (await db.execute(select(UserCredentials).where(UserCredentials.id == response1.id))).scalar()

        if response2 is None:
            raise HTTPException(status_code=400, detail="Пароль для заданного пользователя не найден.")

        is_correct_pwd = UserCredentials.verify_password(form_data.password, cast(bytes, response2.salt), cast(bytes, response2.password_hash))

        if is_correct_pwd:

            access_token = RefreshToken.create_access_token(
                data={"sub": str(response1.id)}
            )
            
            refresh_token = RefreshToken.create_refresh_token(data={"sub": str(response1.id)})

            return Token(
                access_token=access_token,
                refresh_token=refresh_token
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Неверный email или пароль"
            )

login_api_route = LoginRoute()    