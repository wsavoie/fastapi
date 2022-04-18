from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.sql.functions import coalesce
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts'] #groups commands in the swagger docs
)

def get_post_response_by_id(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    return post, post_query

def get_all_post_info_by_id(id: int, db: Session = Depends(get_db)):
    sum_expr = coalesce(func.sum(models.Vote.direction),0).label('score')
    
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label('votes'), sum_expr).join(
                    models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    return post, post_query

def checkIfUserIsCurrent(current_user_id: int, original_user_id: int):
    if current_user_id != original_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user_id: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.user_id=current_user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db),  user_id: Optional[int]=None, limit: int = 10, skip: int = 0, title: Optional[str] = ""):
    filters = [(models.Post.user_id,user_id), (models.Post.title.contains,title)]

    # query = db.query(models.Post)
    sum_expr = coalesce(func.sum(models.Vote.direction),0).label('score')    # coalese
    query = db.query(models.Post, func.count(models.Vote.post_id).label('votes'), sum_expr).join(
                    models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id)
    # for (model,value) in filters:
    #     if value:
    #         query = query.filter(model==value)
    if user_id:
        query = query.filter(models.Post.user_id==user_id)
    if title:
        query = query.filter(models.Post.title.contains(title))

    posts=query.limit(limit).offset(skip).all()
    # sum_expr = coalesce(func.sum(models.Vote.direction),0).label('score')    # coalese

    # results = db.query(models.Post,sum_expr, func.count(models.Vote.post_id).label('votes'), sum_expr).join(
    #                 models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).all()

    if len(posts) == 0:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No posts found")
    return posts

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post, _ = get_all_post_info_by_id(id, db)
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user_id: int = Depends(oauth2.get_current_user)):
    post,post_query = get_post_response_by_id(id, db)
    checkIfUserIsCurrent(current_user_id,post.user_id)
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostOut) #), status_code=status.)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user_id: int = Depends(oauth2.get_current_user)):

    orig_post, orig_post_query = get_post_response_by_id(id, db)
    checkIfUserIsCurrent(current_user_id, orig_post.user_id)
    orig_post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    output_post, _= get_all_post_info_by_id(id, db)
    return output_post

