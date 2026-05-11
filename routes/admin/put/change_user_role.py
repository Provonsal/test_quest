from ...base_route import BaseRoute


class ChangeUserRoleRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'change/user/role'
        self.methods_type = "PUT"

    def endpoint(self):
        ...

change_user_role_route = ChangeUserRoleRoute()    