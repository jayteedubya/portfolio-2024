from dotenv import load_dotenv
load_dotenv()

from db_engine import engine
from routes.posts.posts import Post
from app.routes.users.users import User

from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
