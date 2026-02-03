from api.core.security import password_hash
from api.models.users import USER
from api.schemas.user_schema import UserCreate

def create_user (user : UserCreate):
    hashed_password = password_hash(user.password)
    new_user = USER(email= user.email,username=user.username,password_hash=hashed_password)
    return new_user 