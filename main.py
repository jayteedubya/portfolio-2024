from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from os import getenv

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import posts



app = FastAPI()

app.include_router(posts.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})
