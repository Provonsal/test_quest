from ...base_route import BaseRoute


class ChangeRoleRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'change/role'
        self.methods_type = "PUT"

    def endpoint(self):
        ...

change_role_route = ChangeRoleRoute()    