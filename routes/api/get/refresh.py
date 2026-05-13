from ...base_route import BaseRoute


class RefreshRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'refresh'
        self.methods_type = "GET"

    def endpoint(self):
        ...

refresh_api_route = RefreshRoute()    