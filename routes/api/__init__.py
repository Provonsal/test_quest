from models.forms import UserResponse

from .get import register_api_route

from .api_router import router

router.add_api_route(register_api_route.path, register_api_route.endpoint, methods=register_api_route.methods_type, response_model=UserResponse)