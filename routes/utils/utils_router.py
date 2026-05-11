from fastapi import APIRouter


router = APIRouter(
    prefix="/utils",  # Все пути будут начинаться с /utils
    tags=["utils"],    # Тег для документации
    responses={404: {"description": "Not found"}}  # Общие ответы
)

