
from typing import List

import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users'] #groups commands in the swagger docs
)


def checkIfUserIsCurrent(current_user_id: int, original_user_id: int):
    if current_user_id != original_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not authorized to perform requested action")

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd

    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail=f'Email already exists in database, please select a different email')
    db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db),
                  user_id: int = Depends(oauth2.get_current_user)):
    user = db.query(models.User).all()
    return user


def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f'User with id: {id} does not exist')
    return user, user_query
    
@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user, _ = get_user_by_id(id, db)
    return user

@router.put("/{id}", response_model=schemas.UserResponse) #), status_code=status.)
def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user_id: int = Depends(oauth2.get_current_user)):
    original_user, original_user_query = get_user_by_id(id, db)
    checkIfUserIsCurrent(current_user_id,original_user.id)
    original_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return original_user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
                current_user_id: int = Depends(oauth2.get_current_user)):
    user, user_query = get_user_by_id(id, db)
    checkIfUserIsCurrent(current_user_id,user.id)
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)