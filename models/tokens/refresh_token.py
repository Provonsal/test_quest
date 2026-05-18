from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException

from sqlalchemy.orm import relationship
from sqlalchemy import BINARY, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql.types import BYTEA

from jose import JWTError, jwt

from models.base_model import Base


class RefreshToken(Base):
    """
    Данные профиля пользователя
    """
    __tablename__ = 'refresh_tokens'
    
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    expire_date = Column(Integer, nullable=False)
    revoked = Column(Boolean, nullable=False)
    token_hash = Column(BYTEA(32), nullable=False)
    family_id = Column(UUID(as_uuid=True), nullable=False, default=uuid4)
    
    # Связи
    users = relationship("User", back_populates="refresh_tokens")
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Создание JWT access токена"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        
        return encoded_jwt

    @classmethod
    def create_refresh_token(cls, data: dict) -> str:
        """Создание JWT refresh токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=cls.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        
        return encoded_jwt

    @classmethod
    def decode_token(cls, token: str) -> dict:
        """Декодирование JWT токена"""
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}')>"
    
    def to_dict(self):
        """Конвертация в словарь"""
        
        data = {
            'id': self.id,
            'role': self.role.to_dict() if self.role else None,
            'created_at': self.created_at.isoformat() if self.created_at else None, # pyright: ignore[reportGeneralTypeIssues]
            'is_active': self.is_active
        }
        
        return data
    
    def has_role(self, role_name: str) -> bool:
        """Проверить, имеет ли пользователь указанную роль"""
        return self.role and self.role.name == role_name