from fastapi import HTTPException
from sqlalchemy import select

from models.forms import RefreshToken as RefreshTokenSchema
from db.db import db_dependency
from models import RefreshToken, User
from models.forms import Token

from ...base_route import BaseRoute


class RefreshRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'refresh'
        self.methods_type = "POST"

    async def endpoint(self, refresh_data: RefreshTokenSchema, db: db_dependency):
        try:
            payload = RefreshToken.decode_token(refresh_data.refresh_token)
            
            # Проверяем, что это refresh токен
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token type"
                )
            
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token"
                )
            
            user = (await db.execute(select(User).where(User.id == user_id))).first()

            if not user or not user.is_active:
                raise HTTPException(
                    status_code=401,
                    detail="User not found or inactive"
                )
            
            access_token = RefreshToken.create_access_token(data={"sub": str(user.id)})
            refresh_token = RefreshToken.create_refresh_token(data={"sub": str(user.id)})

            return Token(
                access_token=access_token,
                refresh_token=refresh_token
            )

        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

refresh_api_route = RefreshRoute()    