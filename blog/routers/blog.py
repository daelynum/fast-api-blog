from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from blog import schemas
from blog.database import get_db
from blog.oath2 import get_current_user, get_current_user_id
from blog.schemas import Blog, User, ShowBlog
from blog.repository.blog_code import get_all, get_one_blog, update_blog, destroy_blog, new_blog, get_my_blogs

router = APIRouter(
    prefix='/blog',
    tags=['Blogs']
)


@router.get('/', status_code=200, response_model=List[ShowBlog])
def all_blogs(db: Session = Depends(get_db)):
    """Show all blogs"""

    return get_all(db)


@router.get('/my_blogs/', status_code=status.HTTP_200_OK, response_model=List[ShowBlog])
def all_my_blogs(db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user),
                 current_user_id: User = Depends(get_current_user_id)):
    """Show all my blogs"""
    return get_my_blogs(db, current_user_id)


@router.get('/{blog_id}', status_code=200, response_model=schemas.ShowBlog)
def show_one_blog(blog_id, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user),
                  current_user_id: User = Depends(get_current_user_id)):
    """Show particular blog"""
    return get_one_blog(db, blog_id, current_user_id)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user),
           current_user_id: User = Depends(get_current_user_id)):
    '''Update particular blog'''
    return update_blog(blog_id, request, db, current_user_id)


@router.delete('/{blog_id}', status_code=status.HTTP_200_OK)
def delete(blog_id, db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user),
            current_user_id: User = Depends(get_current_user_id)):
    '''Delete particular blog'''
    return destroy_blog(db, blog_id, current_user_id)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db),
           current_user: User = Depends(get_current_user),
           current_user_id: User = Depends(get_current_user_id)):
    '''Create a blog'''
    return new_blog(db, request, current_user_id)
