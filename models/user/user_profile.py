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
    
    id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=False)
    
    # Связи
    users = relationship("User", back_populates="user_profile")
    
    
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
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name
        }

        if not_none:
            data = self.__remove_none_values(data)
        
        return data
    
    def has_role(self, role_name: str) -> bool:
        """Проверить, имеет ли пользователь указанную роль"""
        return self.role and self.role.name == role_name