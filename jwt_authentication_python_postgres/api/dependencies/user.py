from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from jwt_authentication_python_postgres.api.dependencies.database import get_repository
from jwt_authentication_python_postgres.api.dependencies.settings import get_settings
from jwt_authentication_python_postgres.core.config import Settings
from jwt_authentication_python_postgres.db.repositories.users import UsersRepository
from jwt_authentication_python_postgres.models.token import TokenData
from jwt_authentication_python_postgres.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    settings: Settings = Depends(get_settings),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    try:
        user = await users_repo.get_user(username=username)
    except TypeError:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
