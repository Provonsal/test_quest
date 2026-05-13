from typing import cast

from fastapi import HTTPException
from sqlalchemy import insert, select
from uuid import uuid4

from ...base_route import BaseRoute
from models.forms import UserResponse, UserLogin
from models import User, UserProfile, UserCredentials, Role
from db.db import db_dependency


class LoginRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'login'
        self.methods_type = "POST"

    async def endpoint(self, user: UserLogin, db: db_dependency):

        response1 = (await db.execute(select(User).where(User.email==user.email))).scalar()

        if response1 is None:
            raise HTTPException(status_code=400, detail="Неверный email или пароль")
        
        response2 = (await db.execute(select(UserCredentials).where(UserCredentials.id == response1.id))).scalar()

        if response2 is None:
            raise HTTPException(status_code=400, detail="Пароль для заданного пользователя не найден.")

        is_correct_pwd = UserCredentials.verify_password(user.password, cast(bytes, response2.salt), cast(bytes, response2.password_hash))

        if is_correct_pwd:

            return UserResponse(
                full_name="123",
                email=cast(str, response1.email),
                message="Вход выполнен успешно"
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Неверный email или пароль"
            )

login_api_route = LoginRoute()    