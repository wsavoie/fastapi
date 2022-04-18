from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix='/votes',
    tags=['Votes'] #groups commands in the swagger docs
)
def get_vote_by_id(user_id: int, post_id: int, db: Session = Depends(get_db)):
    
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error applying vote, post with id: {post_id} does not exist")
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == user_id, models.Vote.post_id == post_id)
    vote = vote_query.first()
    # if not vote:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
    #                         detail=f'Post with id: {user_id} does not exist')
    return vote, vote_query

def checkIfUserIsCurrent(current_user_id: int, original_user_id: int):
    if current_user_id != original_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.VoteResponse)
def get_votes(id:int, db: Session = Depends(get_db),current_user_id: int = Depends(oauth2.get_current_user)):
    vote, _ = get_vote_by_id(user_id = current_user_id, post_id = id, db=db)
    return vote

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteResponse)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    vote_out, existing_vote_query = get_vote_by_id(user_id=current_user_id, post_id=vote.post_id, db=db)
    if vote_out:
        if (vote_out.direction > 0 and vote.direction > 0) or (vote_out.direction < 0 and vote.direction < 0):
            vote.direction = 0
        existing_vote_query.update(vote.dict(), synchronize_session=False) 
        db.commit()
    else:
        vote_out = models.Vote(**vote.dict())
        vote_out.user_id = current_user_id
        db.add(vote_out)
        db.commit()
        db.refresh(vote_out)
    return vote_out

@router.put("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VoteResponse)
def update_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    vote_out, existing_vote_query = get_vote_by_id(user_id=current_user_id, post_id=vote.post_id, db=db)
    if vote_out:
        if (vote_out.direction > 0 and vote.direction > 0) or (vote_out.direction < 0 and vote.direction < 0):
            vote.direction = 0
        existing_vote_query.update(vote.dict(), synchronize_session=False) 
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cannot update vote, vote does not exist")
    return vote_out



# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), 
#                  current_user_id: int = Depends(oauth2.get_current_user)):        
#     new_post = models.Post(**post.dict())
#     new_post.user_id=current_user_id
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post

# @router.get("/", response_model=List[schemas.PostResponse])
# def get_all_posts(db: Session = Depends(get_db),  user_id: Optional[int]=None, limit: int = 10, skip: int = 0, title: Optional[str] = ""):
#     filters = [(models.Post.user_id,user_id), (models.Post.title.contains,title)]

#     query = db.query(models.Post)
#     # for (model,value) in filters:
#     #     if value:
#     #         query = query.filter(model==value)
#     if user_id:
#         query = query.filter(models.Post.user_id==user_id)
#     if title:
#         query = query.filter(models.Post.title.ilike(title))

#     posts=query.limit(limit).offset(skip).all()

#     if len(posts) == 0:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="No posts found")
#     return posts
   
# @router.get("/{id}", response_model=schemas.PostResponse)
# def get_post(id: int, db: Session = Depends(get_db)):
#     post, _ = get_post_by_id(id, db)
#     return post


# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db),
#                 current_user_id: int = Depends(oauth2.get_current_user)):
#     post,post_query = get_post_by_id(id, db)
#     checkIfUserIsCurrent(current_user_id,post.user_id)
#     post_query.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/{id}", response_model=schemas.PostResponse) #), status_code=status.)
# def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
#                 current_user_id: int = Depends(oauth2.get_current_user)):
#     orig_post, orig_post_query= get_post_by_id(id, db)
#     checkIfUserIsCurrent(current_user_id,orig_post.user_id)
#     orig_post_query.update(post.dict(), synchronize_session=False)
#     db.commit()
#     return orig_post

