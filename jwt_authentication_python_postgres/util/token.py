from datetime import datetime, timedelta
from fastapi import Depends
from jose import jwt
from typing import Optional

from jwt_authentication_python_postgres.api.dependencies.settings import get_settings


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):
    settings = get_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt
