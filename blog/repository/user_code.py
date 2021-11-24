from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from blog import models, hashing
from blog.schemas import User


def new_user(db: Session, request: User):
    new_user = models.Users(name=request.name,
                            surname=request.surname,
                            email=request.email,
                            # пароль хэшируется посредством функции из файла hashing.py
                            password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_one_user(db: Session, id: int):
    one_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not one_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with the id = {id} is not available')
    return one_user
