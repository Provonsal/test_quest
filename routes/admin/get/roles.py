from ...base_route import BaseRoute


class RolesRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'roles'
        self.methods_type = "GET"

    def endpoint(self):
        ...

roles_route = RolesRoute()    