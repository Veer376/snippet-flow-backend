from pydantic import BaseModel

class User(BaseModel):
    email: str
    
class UserInDB(User):
    hashed_password: str

class Interaction(BaseModel):
    userid: int
    snippetid: int
    rating: int
