from datetime import datetime, timezone
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