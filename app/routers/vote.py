from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import oauth2, models, schemas
from ..database import get_db


router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ## schemas.Vote -> (pydantic model)
    ## vote.post_id -> post id provided by the end user (pydantic model)
    ## models.Vote.post_id -> post id in the Vote table (sqlalchemy model)
    ## .filter -> WHERE condition
    ## vote.dir = 1 (if vote found -> raise HTTPException, if vote not found -> create new vote)
    ## vote.dir = 0 (if vote found -> delete the vote, if vote not found -> raise HTTPException)
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {vote.post_id} was not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        ## if the user has already voted on the post
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        ## if the vote doesn't exist
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        
        db.add(new_vote)
        db.commit()
        
        return {"message": "vote added"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "vote deleted"}