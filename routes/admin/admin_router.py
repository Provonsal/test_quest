from fastapi import APIRouter


router = APIRouter(
    prefix="/admin",  # Все пути будут начинаться с /users
    tags=["admins"],    # Тег для документации
    responses={404: {"description": "Not found"}}  # Общие ответы
)