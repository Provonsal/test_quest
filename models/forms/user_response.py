from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    full_name: str
    email: EmailStr
    message: str