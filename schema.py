from pydantic import BaseModel

class User(BaseModel):
    email: str
    
class UserInDB(User):
    hashed_password: str

class Interaction(BaseModel):
    user_id: int
    snippet_id: int
    rating: int

class Snippet(BaseModel):
    text: str
    author: str | None
    
