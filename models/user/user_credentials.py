from datetime import datetime, timezone
import hashlib
import secrets
from typing import Tuple
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import BINARY, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql.types import BYTEA

from models.base_model import Base


class UserCredentials(Base):
    """
    Данные профиля пользователя
    """
    __tablename__ = 'user_credentials'
    
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    salt = Column(BYTEA(16), nullable=False)
    password_hash = Column(BYTEA(32), nullable=False)
    algorithm = Column(String(16), nullable=False, index=True)
    
    # Связи
    users = relationship("User", back_populates="user_credentials")
    
    ALGORITHM = "sha256"  # будем хранить в колонке algorithm
    SALT_SIZE = 16        # байт, как у тебя BYTEA(16)
    HASH_SIZE = 32        # байт, как у тебя BYTEA(32)
    ITERATIONS = 600_000  # количество итераций PBKDF2

    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}')>"
    
    @classmethod
    def generate_salt(cls) -> bytes:
        """Генерирует криптографически безопасную соль (16 байт)."""
        return secrets.token_bytes(cls.SALT_SIZE)

    @classmethod
    def hash_password(cls, password: str, salt: bytes) -> bytes:
        """
        Хэширует пароль с солью.
        Возвращает ровно 32 байта.
        """
        # Кодируем пароль в bytes
        password_bytes = password.encode('utf-8')

        # PBKDF2-HMAC-SHA256 с 600 000 итераций
        hash_bytes = hashlib.pbkdf2_hmac(
            'sha256',
            password_bytes,
            salt,
            cls.ITERATIONS,
            dklen=cls.HASH_SIZE   # ровно 32 байта
        )

        return hash_bytes

    @classmethod
    def create_credentials(cls, password: str) -> Tuple[bytes, bytes]:
        """
        Создаёт пару (salt, password_hash) для нового пользователя.
        """
        salt = cls.generate_salt()
        hash_bytes = cls.hash_password(password, salt)
        return salt, hash_bytes
    
    @classmethod
    def verify_password(cls, password: str, salt: bytes, stored_hash: bytes) -> bool:
        """
        Проверяет пароль.
        Сравнивает через secrets.compare_digest для защиты от timing-атак.
        """
        new_hash = cls.hash_password(password, salt)
        return secrets.compare_digest(new_hash, stored_hash)

    def __remove_none_values(self, data: dict):
        new_data = {}
        for k, v in data.items():
                if v is not None:
                    tmp = data.get(k)
                    if tmp is not None:
                        new_data.update({(k, tmp)})
                else:
                    continue
        
        return new_data

    def to_dict(self, not_none=False):
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