from .user_router import router
from .get import login_route, new_route, profile_route, refresh_route
from .put import profile_change_route


router.add_api_route(login_route.path, login_route.endpoint, methods=login_route.methods_type)
router.add_api_route(new_route.path, new_route.endpoint, methods=new_route.methods_type)
router.add_api_route(profile_route.path, profile_route.endpoint, methods=profile_route.methods_type)
router.add_api_route(refresh_route.path, refresh_route.endpoint, methods=refresh_route.methods_type)
router.add_api_route(profile_change_route.path, profile_change_route.endpoint, methods=profile_change_route.methods_type)
