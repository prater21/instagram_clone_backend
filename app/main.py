from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware import log_middleware
from app.routers import auth, user, post
from . import models
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

models.Base.metadata.create_all(bind=engine)
origins = [
    "http://localhost:3000",
]


app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(post.router, prefix="/post", tags=["post"])


@app.get("/hello")
async def hello():

    return {"message": "hello"}
