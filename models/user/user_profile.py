from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Text

from models.base_model import Base


class UserProfile(Base):
    """
    Данные профиля пользователя
    """
    __tablename__ = 'user_profiles'
    
    id = Column(ForeignKey('users.id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    
    # Связи
    users = relationship("User", back_populates="user_profile")
    
    
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