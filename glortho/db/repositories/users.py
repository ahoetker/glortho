from typing import List

from glortho.db.repositories.base import BaseRepository
from glortho.models.user import (
    UserCreateHashedPassword,
    UserInDB,
)

CREATE_USER_QUERY = """
    INSERT INTO users (username, email, full_name, disabled, hashed_password)
    VALUES (:username, :email, :full_name, :disabled, :hashed_password);
"""

READ_USER_QUERY = """
    SELECT id, username, email, full_name, disabled, hashed_password FROM users
    WHERE username = :username;
"""

READ_USERS_QUERY = """
    SELECT id, username, email, full_name, disabled FROM users;
"""


class UsersRepository(BaseRepository):
    """ "
    All database actions associated with the User resource
    """

    async def create_user(self, *, new_user: UserCreateHashedPassword) -> UserInDB:
        query_values = new_user.dict(exclude={"password"})
        await self.db.fetch_one(query=CREATE_USER_QUERY, values=query_values)
        user = await self.db.fetch_one(query=READ_USER_QUERY, values={"username": new_user.username})
        return UserInDB(**user)

    async def get_user(self, *, username: str) -> UserInDB:
        user = await self.db.fetch_one(
            query=READ_USER_QUERY, values={"username": username}
        )
        return UserInDB(**user)

    async def get_users(self) -> List[UserInDB]:
        users = await self.db.fetch_all(query=READ_USERS_QUERY)
        return [UserInDB(**user) for user in users]
