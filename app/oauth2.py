from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from .config import settings

login_prefix = 'login'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=login_prefix)


SECRET_KEY = settings.secret_key
ALGORITHM  = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict, expires_delta : timedelta | None = None):
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('user_id')
        
        if not user_id:
            raise credentials_exception

        token_data = user_id
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception= HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail=f'Could not validate credentials',
                                        headers={"WWW-Authenticate":"Bearer"})

    #we could return the actual user from the database here, but we are just getting the id for now
    return verify_access_token(token, credentials_exception)


