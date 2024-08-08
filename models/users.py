from pydantic import BaseModel, EmailStr
from models.events import Event


class User(BaseModel):
    email: EmailStr
    username: str
    events: list[Event] | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "fastapi@packt.com",
                    "events": [],
                }
            ]
        }
    }


class NewUser(User):
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "fastapi@packt.com",
                    "password": "strong!!!",
                    "username": "example",
                }
            ]
        }
    }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "fastapi@packt.com",
                    "password": "strong!!!",
                }
            ]
        }
    }
