from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session

from blog import schemas
from blog.database import get_db
from blog.repository.user_code import new_user, get_one_user
from blog.schemas import User

router = APIRouter(
    prefix='/user',  # базовый префикс для всех маршрутов
    tags=['Users']  # тэги для всех маршрутов
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
def create_user(request: User, db: Session = Depends(get_db)):
    return new_user(db, request)


@router.get('/{id}', status_code=200, response_model=schemas.ShowUser)
def show_user(id: int, db: Session = Depends(get_db)):
    return get_one_user(db, id)