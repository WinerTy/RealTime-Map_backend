from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select


class MySQLAlchemyUserDatabase(SQLAlchemyUserDatabase):
    def __init__(self, session, user_table):
        super().__init__(session, user_table)

    async def get_by_phone(self, phone: str):
        stmt = select(self.user_table).where(self.user_table.phone == phone)
        return await self._get_user(stmt)

    async def get_by_username(self, username: str):
        stmt = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(stmt)

    async def validate_user_credentials(self, phone: str, username: str, email: str):
        stmt = select(self.user_table).where(
            (self.user_table.phone == phone)
            | (self.user_table.username == username)
            | (self.user_table.email == email),
        )
        return await self._get_user(stmt)
