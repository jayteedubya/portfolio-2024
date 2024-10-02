from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pw_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/signin")