from .user_router import router
from .get import login_route, profile_route
from .put import profile_change_route


router.add_api_route(login_route.path, login_route.endpoint, methods=login_route.methods_type)
router.add_api_route(profile_route.path, profile_route.endpoint, methods=profile_route.methods_type)
router.add_api_route(profile_change_route.path, profile_change_route.endpoint, methods=profile_change_route.methods_type)
