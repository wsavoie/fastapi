import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES

from . import models, utils
from .config import settings
from .database import engine
from .routers import auth, post, user, vote

#below line creates tables which don't exist already using sql alchemy, we instead use alembic because it is more powerful
# models.Base.metadata.create_all(bind=engine) 


app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/test/{p1}-{p2}")
def test_func(p1,p2):
    h1,h2 = utils.hash(p1), utils.hash(p2)
    print(h1==h2)
    return h1,h2,p1,p2

