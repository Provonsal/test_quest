from models.forms import UserResponse, Token

from .post import register_api_route, login_api_route, refresh_api_route, logout_api_route

from .api_router import router

router.add_api_route(register_api_route.path, register_api_route.endpoint, methods=register_api_route.methods_type, response_model=UserResponse)
router.add_api_route(login_api_route.path, login_api_route.endpoint, methods=login_api_route.methods_type, response_model=Token)
router.add_api_route(refresh_api_route.path, refresh_api_route.endpoint, methods=refresh_api_route.methods_type, response_model=Token)
router.add_api_route(logout_api_route.path, logout_api_route.endpoint, methods=logout_api_route.methods_type)