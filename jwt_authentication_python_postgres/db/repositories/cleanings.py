from jwt_authentication_python_postgres.db.repositories.base import BaseRepository
from jwt_authentication_python_postgres.models.cleaning import (
    CleaningCreate,
    CleaningUpdate,
    CleaningInDB,
)
from typing import List

CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type)
    VALUES (:name, :description, :price, :cleaning_type)
    RETURNING id, name, description, price, cleaning_type;
"""

READ_CLEANING_QUERY = """
    SELECT * FROM cleanings WHERE id = :id;
"""

READ_CLEANINGS_QUERY = """
    SELECT * FROM cleanings;
"""

DELETE_CLEANING_QUERY = """
    DELETE FROM cleanings
    WHERE id = :id
    RETURNING id, name, description, price, cleaning_type;
"""


class CleaningsRepository(BaseRepository):
    """ "
    All database actions associated with the Cleaning resource
    """

    async def create_cleaning(self, *, new_cleaning: CleaningCreate) -> CleaningInDB:
        query_values = new_cleaning.dict()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY, values=query_values
        )
        return CleaningInDB(**cleaning)

    async def get_cleaning(self, *, id: int) -> CleaningInDB:
        cleaning = await self.db.fetch_one(query=READ_CLEANING_QUERY, values={"id": id})
        return CleaningInDB(**cleaning)

    async def get_cleanings(self) -> List[CleaningInDB]:
        cleanings = await self.db.fetch_all(query=READ_CLEANINGS_QUERY)
        return [CleaningInDB(**cleaning) for cleaning in cleanings]

    async def delete_cleaning(self, *, id: int) -> CleaningInDB:
        cleaning = await self.db.fetch_one(
            query=DELETE_CLEANING_QUERY, values={"id": id}
        )
        return CleaningInDB(**cleaning)
