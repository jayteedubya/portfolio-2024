from typing import Annotated

from templates import templates
from db_engine import engine
from routes.auth.auth import pw_context

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from sqlmodel import Field, SQLModel, Relationship, DateTime, Session, select
from pydantic import BaseModel


router = APIRouter(prefix="/users")

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_password: str
    role: str

class SignUpForm(BaseModel):
    username: str
    password: str
    confirm_password: str

@router.get("/new", response_class=HTMLResponse)
async def new_user_view(request: Request):
    return templates.TemplateResponse(request=request, name="new_user.html", context={})

@router.post("/new")
async def new_user(user_form: Annotated[SignUpForm, Form()]):
    new_user = User(username = user_form.username, hashed_password=pw_context.hash(user_form.password), role="standard")
    
    with Session(engine) as sess:
        sess.add(new_user)
        sess.commit()

@router.get("/")
async def users(request: Request):
    statement = select(User)
    with Session(engine) as sess:
        result = sess.exec(statement)
        return templates.TemplateResponse(request=request, name="users.html", context={"users": [item.username for item in result.all()]})