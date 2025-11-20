
from ninja import Schema

class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access: str
    refresh: str

class ErrorSchema(Schema):
    error: str