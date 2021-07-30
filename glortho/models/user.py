from email_validator import validate_email, EmailNotValidError
from typing import Optional
from glortho.models.core import IDModelMixin, CoreModel
from pydantic import constr, validator


class UserBase(CoreModel):
    username: Optional[str]
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = False

    @validator("email")
    def email_valid(cls, v):
        if v is None:
            return None
        else:
            try:
                valid = validate_email(v)
                return valid.email
            except EmailNotValidError as e:
                raise ValueError(e)


class UserCreate(UserBase):
    username: constr(to_lower=True, min_length=3, max_length=30)
    password: constr(min_length=8, max_length=30)


class UserCreateHashedPassword(UserCreate):
    hashed_password: str


class UserUpdate(CoreModel):
    email: Optional[str]
    full_name: Optional[str]
    diabled: Optional[bool]

    @validator("email")
    def email_valid(cls, v):
        try:
            valid = validate_email(v)
            return valid
        except EmailNotValidError as e:
            raise ValueError(e.detail)


class UserInDB(IDModelMixin, UserBase):
    username: str
    hashed_password: str


class User(UserInDB):
    pass


class UserPublic(IDModelMixin, UserBase):
    pass
