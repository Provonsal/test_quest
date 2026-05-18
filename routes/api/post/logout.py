from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from models import User
from utils.auth import get_current_user

from ...base_route import BaseRoute


class LogoutRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'login'
        self.methods_type = "POST"

    async def endpoint(self, current_user: User = Depends(get_current_user)):
        """Выход из системы (на клиенте нужно удалить токен)"""
        return {"message": "Successfully logged out"}
        

logout_api_route = LogoutRoute()   