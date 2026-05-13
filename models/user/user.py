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
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id', ondelete='SET NULL'), nullable=False)
    email = Column(String(60), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Связи
    role = relationship("Role", back_populates="users")
    user_profile = relationship("UserProfile", back_populates="users")
    user_credentials = relationship("UserCredentials", back_populates="users")
    refresh_tokens = relationship("RefreshToken", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, login='{self.login}')>"

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
            'role_id': self.role_id,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at is not None else None, 
            'is_active': self.is_active
        }

        if not_none:
            data = self.__remove_none_values(data)
        
        return data
    
    def has_role(self, role_name: str) -> bool:
        """Проверить, имеет ли пользователь указанную роль"""
        return self.role and self.role.name == role_name