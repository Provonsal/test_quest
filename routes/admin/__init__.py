from .put import change_role_route, change_user_role_route
from .get import profile_route, roles_route
from .admin_router import router


router.add_api_route(change_role_route.path, change_role_route.endpoint, methods=change_role_route.methods_type)
router.add_api_route(change_user_role_route.path, change_user_role_route.endpoint, methods=change_user_role_route.methods_type)
router.add_api_route(profile_route.path, profile_route.endpoint, methods=profile_route.methods_type)
router.add_api_route(roles_route.path, roles_route.endpoint, methods=roles_route.methods_type)