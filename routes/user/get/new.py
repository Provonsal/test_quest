from ...base_route import BaseRoute


class NewRoute(BaseRoute):

    def __init__(self) -> None:
        self.path = 'new'
        self.methods_type = "GET"

    def endpoint(self):
        ...

new_route = NewRoute()    