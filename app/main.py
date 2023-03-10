import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

## Creates all the SQLAlchemy Models/Tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "one coffee a day, keeps the doctor away!!!!!!!!!!!"}
