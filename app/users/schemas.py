from pydantic import BaseModel, EmailStr
from app.events.schemas import EventSchema


class UserSchema(BaseModel):
    email: EmailStr
    username: str
    events: list[EventSchema] | None = None

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


class UserCreateSchema(BaseModel):
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


class UserSignInSchema(BaseModel):
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
