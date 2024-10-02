from os import getenv
from typing import Annotated

from app.templates import templates
from app.db_engine import engine
from app.routes.users.users import User
from app.routes.auth.context import oauth2_scheme, pw_context
from app.routes.auth.models import Token, TokenData, SignInForm

from fastapi import APIRouter, Request, Form, HTTPException, Depends, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from sqlmodel import Session, select
import jwt



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, getenv("SECRET_KEY"), algorithms=[getenv("ALGORITHM")])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user





router = APIRouter(prefix="/auth")

@router.get("/signin", response_class=HTMLResponse)
def sign_in_view(request: Request):
    return templates.TemplateResponse(request=request, name="signin.html", context={})

@router.post("/signin", response_class=JSONResponse)
def sign_in(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    password = form_data.password
    username = form_data.username
    with Session(engine) as sess:
        user_in_db: User = sess.exec(select(User).where(User.username == username)).one()
        pw_valid = pw_context.verify(secret=password, hash=user_in_db.hashed_password)
    if not pw_valid:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user_in_db.username, "token_type": "bearer"}

