from pydantic import BaseModel



class UserBase(BaseModel):
    email: str
    password :str
    

class UserCreate(UserBase):
    username : str
    

class UserLogin(UserBase):
    pass 


class User(UserBase):
    id: int
    is_active: bool
    password_hash : str 


