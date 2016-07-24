import asyncio

import sqlalchemy as sa

from demo import settings


def init_db():
    dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(
        user=settings.DB_USER,
        database=settings.DATABASE,
        host=settings.DB_HOST,
        password=settings.DB_PASSWORD
    )
    metadata = sa.MetaData()
    engine = sa.create_engine(dsn)

    metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
