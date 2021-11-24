from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from blog.database import get_db
from blog.schemas import TokenData
from blog.token import verify_token, SECRET_KEY, ALGORITHM
from blog import models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)


def get_user_id(db, email: str):
    if email in db.query(models.Users.email):
        user_id = db.query(models.Users).filter(models.Users.email == email)
        return user_id


def get_current_user_id(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(name=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Users).filter(models.Users.email == token_data.name).first()
    if user is None:
        raise credentials_exception
    return user.id
