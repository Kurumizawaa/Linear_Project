from pydantic import BaseModel

class Login(BaseModel):
    username: str
    password: str

class Signup(BaseModel):
    username: str
    password: str