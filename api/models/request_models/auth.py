from typing import Optional
from pydantic import BaseModel


class AuthRequest(BaseModel):
    token: str


class AuthRequestWithName(AuthRequest):
    username: str
    first_name: str
    last_name: str


class ProfileChangePasswordRequest(BaseModel):
    email: str
    old_password: str
    new_password: str
    confirm_new_password: str


class ProfileUpdateRequest(BaseModel):
    uid: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
