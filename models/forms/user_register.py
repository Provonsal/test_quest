from typing import Optional

from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    email: EmailStr
    password: str