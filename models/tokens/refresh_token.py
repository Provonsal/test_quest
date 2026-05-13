from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import BINARY, UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql.types import BYTEA

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