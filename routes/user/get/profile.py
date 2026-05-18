from fastapi import Depends, Request

from models import User
from templates import templates
from utils.auth import get_current_user

from ...base_route import BaseRoute


class ProfileRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'profile'
        self.methods_type = "GET"

    def endpoint(self, request: Request, current_user: User = Depends(get_current_user)):
        return templates.TemplateResponse(
            request, 
            "after_logging_in_dummy.html", 
            {"user": current_user}
        )

profile_route = ProfileRoute()    