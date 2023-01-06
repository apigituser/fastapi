from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import utils
from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hashing the user password
    user.password = utils.hash(user.password)

    email_exists = db.query(models.User).filter(models.User.email == user.email).first()

    ## if the email exists already in the db then return email exists
    if email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user with email {user.email} already exists")
    
    new_user = models.User(**user.dict())   # Unpacking the dictionary

    db.add(new_user)
    db.commit()
    db.refresh(new_user)                    # Returning the new post

    return new_user
    


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} not found")

    return user.first()