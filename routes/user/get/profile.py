from fastapi import Request

from templates import templates

from ...base_route import BaseRoute


class ProfileRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'profile'
        self.methods_type = "GET"

    def endpoint(self, request: Request):
        return templates.TemplateResponse(request, "after_logging_in_dummy.html")

profile_route = ProfileRoute()    