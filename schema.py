from pydantic import BaseModel
from typing import Optional

class User(BaseModel): # /get
    id: int|None = None # it is not required but to make the queries easy we are keeping it, its optional because it will be used in /auth
    email: str
    
class UserInDB(User): # /auth
    hashed_password: str

class Interaction(BaseModel): # /rating
    user_id: int
    snippet_id: int
    rating: int

class Snippet(BaseModel): # /publish & /consume
    id: int|None = None 
    text: str
    author: str|None = None
    
