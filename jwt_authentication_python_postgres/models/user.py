from typing import Optional
from jwt_authentication_python_postgres.models.core import IDModelMixin, CoreModel


class UserBase(CoreModel):
    username: Optional[str]
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False


class UserCreate(UserBase):
    username: str


class UserCreateHashedPassword(UserCreate):
    hashed_password: str


class UserUpdate(CoreModel):
    email: Optional[str]
    full_name: Optional[str]
    diabled: Optional[bool]


class UserInDB(IDModelMixin, UserBase):
    username: str
    hashed_password: str


class User(UserInDB):
    pass


class UserPublic(IDModelMixin, UserBase):
    pass
