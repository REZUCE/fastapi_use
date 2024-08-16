from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    access_token: str
    user_id: int
