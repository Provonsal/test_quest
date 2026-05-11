from ...base_route import BaseRoute


class AuthRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'auth'
        self.methods_type = "GET"

    def endpoint(self):
        ...

auth_route = AuthRoute()    