from glortho.models.core import IDModelMixin, CoreModel
from typing import Optional


class Token(CoreModel):
    access_token: str
    token_type: str


class TokenData(CoreModel):
    username: Optional[str] = None
