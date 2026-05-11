from ...base_route import BaseRoute


class ProfileRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'profile'
        self.methods_type = "GET"

    def endpoint(self):
        ...

profile_route = ProfileRoute()    