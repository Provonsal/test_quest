from fastapi import APIRouter


router = APIRouter(
    prefix="/api",  # Все пути будут начинаться с /users
    tags=["api"],    # Тег для документации
    responses={404: {"description": "Not found"}}  # Общие ответы
)


