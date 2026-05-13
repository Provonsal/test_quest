from fastapi import Request

from templates import templates

from ...base_route import BaseRoute


class LoginRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'login'
        self.methods_type = "GET"

    def endpoint(self, request: Request):
        return templates.TemplateResponse(request, "auth.html")

login_route = LoginRoute()