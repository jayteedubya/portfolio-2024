from datetime import datetime, timedelta, timezone
from os import getenv
from copy import copy

import jwt
from sqlmodel import Session, select

from ...db_engine import engine
from ..users.users import User

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, getenv("SECRET_KEY"), algorithm=getenv("ALGORITHM"))
    return encoded_jwt


def get_user(username: str) -> User:
    with Session(engine) as sess:
        user_in_db: User = sess.exec(select(User).where(User.username == username)).one()
        return user_in_db