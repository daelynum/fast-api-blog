from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

from blog import models, schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def get_one_blog(db: Session, blog_id: int, user_id: int):
    blog_auth_user = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).first()
    if not blog_auth_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'blog with id {blog_id} not found or belongs to another user')
    return blog_auth_user


def get_my_blogs(db: Session, user_id: id):
    my_blogs = db.query(models.Blog).filter(models.Blog.user_id == user_id).all()
    return my_blogs


def update_blog(blog_id: int, request: schemas.Blog, db: Session, user_id: int):
    blog_auth_user = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).first()
    if not blog_auth_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'blog with id {blog_id} not found or belongs to another user')
    else:
        db.query(models.Blog).filter(models.Blog.id == blog_id).update({
            "title": request.title,
            "body": request.body
        }, synchronize_session='evaluate')
    db.commit()
    return {'data': f'Blog with id№{blog_id} successfully updated'}


def destroy_blog(db: Session, blog_id: int, user_id: int):
    blog_auth_user = db.query(models.Blog).filter(models.Blog.id == blog_id, models.Blog.user_id == user_id).first()
    if not blog_auth_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'blog with id {blog_id} not found or belongs to another user')
    else:
        db.query(models.Blog).filter(models.Blog.id == blog_id).delete(synchronize_session=False)
    db.commit()
    return {'data': f'Blog with id№{blog_id} successfully deleted'}


def new_blog(db: Session, request: schemas.Blog, user_id: id):
    new_blog = models.Blog(title=request.title,
                           body=request.body,
                           user_id=user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog
