from dotenv import load_dotenv
load_dotenv()

from .templates import templates

from typing import Annotated
from os import getenv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import routes.posts.posts as posts
import routes.users.users as users
import routes.auth.auth as auth



app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
