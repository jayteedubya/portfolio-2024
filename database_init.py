from engine import engine
from models import Base

Base.metadata.create_all(engine)
