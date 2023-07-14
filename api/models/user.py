from typing import List
from pydantic import BaseModel


class User(BaseModel):
    _id: str
    username: str
    email: str
    profile_picture: str
    registered_at: str
    last_logged_in: str
    roles: List[str]
