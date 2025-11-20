from pydantic import BaseModel

class Register(BaseModel):
    User_name: str
    email_id: str
    password: str

class RegisterResponse(BaseModel):
    User_name: str
    email_id: str
    password: str

class Login(BaseModel):
    email_id: str
    password: str

class LoginResponse(BaseModel):
    message: str
    user_id: int
