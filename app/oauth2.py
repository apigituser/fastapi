from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
EXPIRATION_TIME = settings.access_token_expire_minutes


def create_token(payload: dict):
    '''
    Modification:
        Adding jwt expiry date to the payload
    '''    
    ## Copying the payload provided by the user
    to_encode = payload.copy()

    ## Creating expiration time of the token
    expire = datetime.utcnow() + timedelta(minutes=EXPIRATION_TIME)

    ## Updating the payload by adding the jwt expiry date 
    to_encode.update({"exp":expire})
    
    ## Encoding the token by providing respective parameters
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenPayload(id=id)    # verifies token schema
        
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Unable to validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_token(token, credentials_exception)
