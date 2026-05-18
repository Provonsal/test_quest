from typing import Any, cast

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError
from sqlalchemy import select

from uuid import UUID


from models import User, RefreshToken
from db.db import db_dependency


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


async def get_current_user(
    db: db_dependency,
    token: str = Depends(oauth2_scheme)
) -> User:
    """Получение текущего пользователя по JWT токену"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload: dict[str, Any] = RefreshToken.decode_token(token)
        user_id: str | None = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        # Проверяем, что это access токен
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )
            
    except JWTError:
        raise credentials_exception
    
    # Получаем пользователя из БД
    user = (await db.execute(select(User).where(User.id == UUID(user_id)))).scalar()
    
    if user is None:
        raise credentials_exception

    if not cast(bool, user.is_active):
        raise HTTPException(
            status_code=403,
            detail="Inactive user"
        )
    
    return user