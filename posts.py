from typing import Optional, Annotated
from datetime import datetime

from templates import templates
from db_engine import engine

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Field, SQLModel, Relationship, DateTime, Session, select

router = APIRouter(prefix="/posts")

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    body: str
    topic: str
    date: Optional[datetime] = Field(default=datetime.now())

@router.get("/all/", response_class=JSONResponse)
async def get_all_posts(sort_by: Optional[str] = None):
    with Session(engine) as sess:
        if sort_by == "topic":
            statement = select(Post).order_by(Post.topic)
        else:
            statement = select(Post).order_by(Post.date)
        query_result = sess.exec(statement)
        return list(query_result)
    
@router.get("/new/", response_class=HTMLResponse)
async def new_post_view(request: Request):
    return templates.TemplateResponse(request=request, name="new_post.html", context={})

@router.post("/new/")
async def new_post_create(post: Annotated[Post, Form()]):
    with Session(engine) as sess:
        sess.add(post)
        sess.commit()