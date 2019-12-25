import asyncpg
from pypika import Table

from appfollow_test import config


posts = Table('posts')


class DB:
    def __init__(self):
        self.pool = None

    async def start(self):
        self.pool = await asyncpg.create_pool(
            dsn=config.get_postgres_dsn(),
        )

    async def close(self):
        await self.pool.close()

    async def execute(self, query, *args, **kwargs):
        sql = query.get_sql()

        return await self.pool.execute(
            sql,
            *args,
            **kwargs
        )

    async def fetch(self, query, *args, **kwargs):
        sql = query.get_sql()

        result = await self.pool.fetch(sql, *args, **kwargs)

        return [
            dict(row)
            for row in result
        ]


db = DB()
