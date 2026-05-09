from uuid import uuid4

from sqlalchemy import UUID, Column, Integer, String, Text
from sqlalchemy.orm import relationship
from models.base_model import Base


class Role(Base):
    """
    Роль пользователя (admin, user, worker, etc.)
    """
    __tablename__ = 'roles'
    
    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(50), nullable=False, unique=True)
    level = Column(Text, nullable=True)
    
    # Связи: Одна роль может быть у МНОГИХ пользователей
    users = relationship("User", back_populates="role", lazy="select")
    
    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }