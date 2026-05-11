from .get import auth_route, oauth_route
from .utils_router import router

router.add_api_route(auth_route.path, auth_route.endpoint, methods=auth_route.methods_type)
router.add_api_route(oauth_route.path, oauth_route.endpoint, methods=oauth_route.methods_type)