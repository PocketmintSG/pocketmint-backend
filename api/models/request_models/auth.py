from pydantic import BaseModel


class AuthRequest(BaseModel):
    token: str


class ProfileChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str
    confirm_new_password: str
