from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from models.base_model import Base


class User(Base):
    """
    Пользователь системы
    """
    __tablename__ = 'users'
    
    id = Column(UUID, primary_key=True, default=uuid4)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'), nullable=False)
    email = Column(String(60), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    role = relationship("Role", back_populates="users")
    user_profile = relationship("UserProfile", back_populates="users")
    user_credentials = relationship("UserCredentials", back_populates="users")
    
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