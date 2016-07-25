import asyncio

import term
import sqlalchemy as sa

from aiopg.sa import create_engine

from demo import settings
from demo.db import metadata, users, permissions


def init_db():
    dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(
        user=settings.DB_USER,
        database=settings.DATABASE,
        host=settings.DB_HOST,
        password=settings.DB_PASSWORD
    )
    term.writeLine('Creating all tables on {dsn}'.format(dsn=dsn), term.bold)
    engine = sa.create_engine(dsn)

    metadata.create_all(engine)
    term.writeLine('{count} tables are successfully '
                   'created!'.format(count=len(metadata.tables)),
                   term.green)


async def create_demo_users(loop=None):
    dbengine = await create_engine(user=settings.DB_USER,
                                   password=settings.DB_PASSWORD,
                                   database=settings.DATABASE,
                                   host=settings.DB_HOST)

    term.writeLine('Inserting users into database...')
    async with dbengine.acquire() as conn:
        await conn.execute(users.insert().values(
            id=1, login='admin', password='admin_pass', is_superuser=True
        ))

        await conn.execute(users.insert().values(
            id=2, login='editor', password='editor_pass'
        ))

        await conn.execute(users.insert().values(
            id=3, login='user', password='user_pass'
        ))

    term.writeLine('Setting permissions on users...')
    async with dbengine.acquire() as conn:
        await conn.execute(permissions.insert().values(
            user_id=2, perm_name='protected'
        ))
        await conn.execute(permissions.insert().values(
            user_id=2, perm_name='public'
        ))
        await conn.execute(permissions.insert().values(
            user_id=3, perm_name='public'
        ))

    term.writeLine('All data has been inserted!', term.green)


def main():
    init_db()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_demo_users(loop))


if __name__ == '__main__':
    main()
