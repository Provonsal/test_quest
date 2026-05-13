from models.forms import UserResponse

from .post import register_api_route, login_api_route

from .api_router import router

router.add_api_route(register_api_route.path, register_api_route.endpoint, methods=register_api_route.methods_type, response_model=UserResponse)
router.add_api_route(login_api_route.path, login_api_route.endpoint, methods=login_api_route.methods_type, response_model=UserResponse)