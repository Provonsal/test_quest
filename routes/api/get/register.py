from fastapi import HTTPException
from sqlalchemy import insert, select
from uuid import uuid4

from ...base_route import BaseRoute
from models.forms import UserResponse, UserRegister
from models import User, UserProfile, UserCredentials, Role
from db.db import db_dependency


class RegisterRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'register'
        self.methods_type = "POST"

    async def endpoint(self, user: UserRegister, db: db_dependency):

        response1 = await db.execute(select(User).where(User.email==user.email))

        if response1.first() is not None:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")

        response2 = (await db.execute(select(Role).where(Role.name=="user"))).scalar()

        if response2 is not None:
            role = response2
        else:
            raise HTTPException(status_code=500, detail="Ошибка сервера")

        new_user = User(
            id=uuid4(), # pyright: ignore[reportCallIssue] # type: ignore
            email=user.email,
            role_id=role.id
        )

        new_user_profile = UserProfile(
            id=new_user.id,
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name
        )

        salt, hash_pwd = UserCredentials.create_credentials(user.password)

        new_user_creds = UserCredentials(
            id=new_user.id,
            salt=salt,
            password_hash=hash_pwd,
        )

        await db.execute(insert(User).values(new_user.to_dict(not_none=True)))
        await db.execute(insert(UserProfile).values(new_user_profile.to_dict()))
        await db.execute(insert(UserCredentials).values(new_user_creds.to_dict(not_none=True)))

        return UserResponse(
            full_name="123",
            email=user.email,
            message="Регистрация успешна"
        )

register_api_route = RegisterRoute()    