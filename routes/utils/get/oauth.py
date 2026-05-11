from ...base_route import BaseRoute


class OAuthRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'oauth'
        self.methods_type = "GET"

    def endpoint(self):
        ...

oauth_route = OAuthRoute()    