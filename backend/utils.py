from passlib.context import CryptContext
from database_operations import DatabaseOperations

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db_operations: DatabaseOperations, username: str, password: str):
    user = db_operations.get_user_by_email(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user