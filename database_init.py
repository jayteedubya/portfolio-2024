from dotenv import load_dotenv
load_dotenv()

from db_engine import engine
from posts import Post

from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
