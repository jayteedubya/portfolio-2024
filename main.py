from typing import Annotated

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import Posts
from engine import engine
from sqlalchemy.orm import Session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@app.post("/new")
async def new_post(title: Annotated[str, Form()], body: Annotated[str, Form()]):
    with Session(engine) as sess:
        new_post = Posts(title=title, body=body)
        sess.add(new_post)
        sess.commit()
