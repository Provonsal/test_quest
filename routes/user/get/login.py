from ...base_route import BaseRoute


class LoginRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'login'
        self.methods_type = "GET"

    def endpoint(self):
        ...

login_route = LoginRoute()    