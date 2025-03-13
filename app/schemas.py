from re import sub
from click import group
from pydantic import BaseModel
from typing import List, Literal, Optional

class User(BaseModel):
    name: str
    last_name:str
    
class UserCreate(User):
    role: Literal['student', 'teacher']
    group: Optional[Literal['A', 'B', 'C', 'D', 'E', 'F']] = None
    semester: Optional[int] = None
    subject: Optional[Literal["Geography", "Mathematics", "English"]] = None

class UserCreateOut(User):
    group: Optional[str] = None
    semester: Optional[int] = None
    subject: Optional[str] = None
    password: str
    email: str
    """
    The response model for the create_user endpoint will return password
    to make it possible for me to log in after creating the user.
    in production, this should be removed. After craeting the user,
    he should have to reset his password for his own security.
    """
    class config:
        from_attributes = True

