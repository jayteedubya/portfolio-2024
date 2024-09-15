from os import getenv
from sqlmodel import create_engine

engine = create_engine(getenv("DB_CONN_STRING"))