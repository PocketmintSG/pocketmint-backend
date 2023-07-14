from pydantic import BaseModel


class LoginRequest(BaseModel):
    token: str
