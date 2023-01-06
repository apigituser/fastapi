from fastapi import HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import get_db

router = APIRouter(
    ## tags -> Makes a separate column in the documentation
    tags=['Authentication']
)

@router.post("/login", response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    ## Verifying users PLAIN-TEXT password with the HASHED password
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")
    
    ## Creating a jwt token with providing a payload
    jwt_token = oauth2.create_token(payload = {"user_id": user.id})
    
    ## Returning the access token with the token type
    return {"access_token": jwt_token, "token_type": "bearer"}