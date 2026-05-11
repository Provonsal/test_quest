from ...base_route import BaseRoute


class ProfileChangeRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'profile'
        self.methods_type = "PUT"

    def endpoint(self):
        ...

profile_change_route = ProfileChangeRoute()    